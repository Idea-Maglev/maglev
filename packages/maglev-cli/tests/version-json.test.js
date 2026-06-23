const { execSync } = require('child_process');
const { test, describe } = require('node:test');
const assert = require('node:assert');
const path = require('path');

const CLI_PATH = path.join(__dirname, '../bin/index.js');

function runCli(args = '') {
  try {
    const output = execSync(`node "${CLI_PATH}" ${args}`, {
      encoding: 'utf8',
      env: { ...process.env, NODE_ENV: 'test' },
    });
    return { stdout: output, exitCode: 0 };
  } catch (err) {
    return { stdout: err.stdout || '', stderr: err.stderr || '', exitCode: err.status };
  }
}

describe('maglev-cli version --json', () => {
  test('outputs valid JSON when --json flag is provided', () => {
    const result = runCli('version --json');
    assert.strictEqual(result.exitCode, 0);
    const parsed = JSON.parse(result.stdout);
    assert.ok(parsed, 'output should be parseable JSON');
  });

  test('JSON contains required fields', () => {
    const result = runCli('version --json');
    assert.strictEqual(result.exitCode, 0);
    const parsed = JSON.parse(result.stdout);
    assert.ok('cli_version' in parsed, 'should have cli_version');
    assert.ok('bundled_version' in parsed, 'should have bundled_version');
    assert.ok('node_version' in parsed, 'should have node_version');
    assert.ok('platform' in parsed, 'should have platform');
  });

  test('cli_version matches package.json version', () => {
    const result = runCli('version --json');
    const parsed = JSON.parse(result.stdout);
    const pkg = require('../package.json');
    assert.strictEqual(parsed.cli_version, pkg.version);
  });

  test('plain version output still works (backward compat)', () => {
    const result = runCli('version');
    // Plain output should NOT be JSON
    assert.throws(() => JSON.parse(result.stdout), 'plain output should not be JSON');
    assert.ok(result.stdout.includes('maglev-cli:'), 'should include maglev-cli: prefix');
  });

  test('node_version matches current runtime', () => {
    const result = runCli('version --json');
    const parsed = JSON.parse(result.stdout);
    assert.strictEqual(parsed.node_version, process.version);
  });

  test('platform matches current OS', () => {
    const result = runCli('version --json');
    const parsed = JSON.parse(result.stdout);
    assert.strictEqual(parsed.platform, process.platform);
  });
});
