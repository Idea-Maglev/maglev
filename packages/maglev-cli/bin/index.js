#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const packageJson = require('../package.json');

function hasRequiredDistArtifacts(distDir) {
  const installerPath = path.join(distDir, 'maglev_installer.py');
  const manifestPath = path.join(distDir, 'manifest.json');
  return fs.existsSync(installerPath) && fs.existsSync(manifestPath);
}

function readManifestVersion(distDir) {
  const manifestPath = path.join(distDir, 'manifest.json');
  if (!fs.existsSync(manifestPath)) {
    return null;
  }

  try {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    return manifest.version || null;
  } catch (error) {
    return null;
  }
}

function resolveDistDir() {
  const bundledDist = path.join(__dirname, '../dist');
  if (hasRequiredDistArtifacts(bundledDist)) {
    return { distDir: bundledDist, mode: 'bundled' };
  }

  // Development fallback: use release build sandbox if package mirror has not been rebuilt yet.
  const buildDist = path.join(__dirname, '../../../.maglev_build');
  if (hasRequiredDistArtifacts(buildDist)) {
    const buildDistVersion = readManifestVersion(buildDist);
    if (buildDistVersion === packageJson.version) {
      return { distDir: buildDist, mode: 'build-dist' };
    }

    return {
      distDir: buildDist,
      mode: 'build-dist-mismatch',
      buildDistVersion,
    };
  }

  return { distDir: bundledDist, mode: 'missing' };
}

function printVersion() {
  const { distDir } = resolveDistDir();
  const manifestPath = path.join(distDir, 'manifest.json');
  const cliVersion = packageJson.version;

  // Check for --json flag
  const jsonFlag = process.argv.includes('--json');

  if (jsonFlag) {
    const result = { cli_version: cliVersion };

    if (!fs.existsSync(manifestPath)) {
      result.error = 'manifest.json missing';
      result.bundled_version = null;
    } else {
      const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
      result.bundled_version = manifest.version || null;
    }

    result.node_version = process.version;
    result.platform = process.platform;

    console.log(JSON.stringify(result));
    return;
  }

  console.log(`maglev-cli: ${cliVersion}`);

  if (!fs.existsSync(manifestPath)) {
    console.error('\x1b[31m❌ 错误: 包内 manifest.json 缺失，无法确认发行版本。\x1b[0m');
    process.exit(2);
  }

  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const bundledVersion = manifest.version || 'unknown';
  console.log(`bundled-dist: ${bundledVersion}`);

  if (cliVersion !== bundledVersion) {
    console.error('\x1b[31m❌ 错误: CLI 版本与包内发行物版本不一致，请重新打包发布。\x1b[0m');
    process.exit(2);
  }
}

const firstArg = process.argv[2];
if (firstArg === 'version' || firstArg === '--version' || firstArg === '-v') {
  printVersion();
  process.exit(0);
}

// Maglev Distribution Engine - Npx Wrapper (Offline Mode)
console.log("\x1b[36mMaglev Distribution Engine (Npx Entry)\x1b[0m");
console.log("========================================");

// 1. Detect Python Environment
let pythonCmd = '';
try {
  execSync('python3 --version', { stdio: 'ignore' });
  pythonCmd = 'python3';
} catch (e) {
  try {
    execSync('python --version', { stdio: 'ignore' });
    pythonCmd = 'python';
  } catch (err) {
    console.error("\x1b[31m❌ 错误: 未找到 Python。请安装 Python 3.6+ 后重试。\x1b[0m");
    process.exit(1);
  }
}

// 2. Locate embedded installer and local dist directory
const { distDir: localDist, mode: distMode } = resolveDistDir();
const installerPath = path.join(localDist, 'maglev_installer.py');

if (distMode === 'build-dist-mismatch') {
  const buildDistVersion = readManifestVersion(localDist) || 'unknown';
  console.error('\x1b[31m❌ 错误: .maglev_build/ 与 CLI 版本不一致，不能作为开发态回退入口。\x1b[0m');
  console.error(`\x1b[31m   CLI: ${packageJson.version} / .maglev_build: ${buildDistVersion}\x1b[0m`);
  console.error('\x1b[31m   请先执行 release dry-run 同步包内镜像，例如: python3 scripts/maglev_release.py --dry-run --skip-audit\x1b[0m');
  process.exit(2);
}

if (!fs.existsSync(installerPath)) {
  console.error(`\x1b[31m❌ 错误: 离线安装器在包体中缺失: ${installerPath}\x1b[0m`);
  process.exit(1);
}

if (distMode === 'build-dist') {
  console.log('\x1b[33m⚠️  检测到包内镜像未同步，当前回退使用 .maglev_build/ 进行开发态验证。\x1b[0m');
}

// 3. Execute Python Script with arguments
const args = process.argv.slice(2).join(' ');
try {
  // Pass --local-dist pointing to the bundled assets
  console.log("🚀 唤醒离线安装器加载内置全系列资产...");
  execSync(`${pythonCmd} "${installerPath}" ${args} --local-dist "${localDist}"`, { stdio: 'inherit' });
  process.exit(0);
} catch (execErr) {
  process.exit(execErr.status || 1);
}
