<div align="center">
  <a href="https://github.com/Reloaded-Project/devops-rust-test-and-coverage" target="_blank">
    <img src="assets/reloaded-logo.png" alt="Logo" width="100" height="100">
  </a>

  <h1 align="center">Reloaded Rust Test and Coverage GitHub Action</h1>

  <p align="center">
    <a href="https://github.com/Reloaded-Project/devops-rust-test-and-coverage/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
  </p>
</div>

This GitHub Action allows you to easily run tests for your Rust library and upload the coverage results to Codecov. It supports various configurations, including specifying the Rust toolchain, target platform, features, and more.

## Features

- 🦀 Test your Rust library using `cargo` or `cross`
- 📊 Optional coverage reports using Tarpaulin (only when using `cargo`)
- ⚡ Fast Tarpaulin installation via `cargo binstall`
- 📤 Upload coverage results to Codecov (only when using `cargo` and Tarpaulin)
- 🛠️ Customize Rust toolchain and target platform
- 📦 Enable or disable default features
- 🔧 Specify additional features to test with
- 💾 Optional Rust toolchain caching for faster builds
- 🎛️ Pass additional arguments to the `cargo test` command

## Usage

To use this action in your GitHub workflow, add the following step:

```yaml
- name: Run Tests and Upload Coverage
  uses: Reloaded-Project/devops-rust-test-and-coverage@v1
  with:
    rust-project-path: '.'
    rust-toolchain: 'stable'
    target: 'x86_64-unknown-linux-gnu'
    install-rust-toolchain: true
    setup-rust-cache: true
    use-tarpaulin: true
    use-binstall: true
    install-binstall: true
    upload-coverage: true
    codecov-token: ${{ secrets.CODECOV_TOKEN }}
    codecov-flags: 'unittests'
    codecov-name: 'codecov-umbrella'
    features: 'feature1 feature2'
    no-default-features: false
    use-cross: false
    additional-test-args: '--ignored --test-threads=1'
```

## Inputs

| Input                    | Description                                                                   | Required | Default              |
| ------------------------ | ----------------------------------------------------------------------------- | -------- | -------------------- |
| `rust-project-path`      | Path to the Rust project                                                      | No       | `'.'`                |
| `rust-toolchain`         | Rust toolchain to use for building and testing (e.g., stable, nightly)        | No       | `'stable'`           |
| `target`                 | The target platform for the Rust compiler                                     | No       | `''`                 |
| `install-rust-toolchain` | Whether to install the specified Rust toolchain                               | No       | `true`               |
| `setup-rust-cache`       | Whether to set up Rust caching                                                | No       | `true`               |
| `use-tarpaulin`          | Whether to use Tarpaulin for code coverage. If false, only runs tests.        | No       | `true`               |
| `use-binstall`           | Use `cargo-binstall` for installing tarpaulin. Else uses cargo install.       | No       | `true`               |
| `install-binstall`       | Installs `cargo-binstall`. If false, assumes it is already available.         | No       | `true`               |
| `upload-coverage`        | Whether to upload coverage to Codecov (only when using `cargo` and Tarpaulin) | No       | `true`               |
| `codecov-token`          | Codecov token for uploading coverage                                          | No       | N/A                  |
| `codecov-flags`          | Flags to pass to Codecov                                                      | No       | `'unittests'`        |
| `codecov-name`           | Custom defined name for the upload                                            | No       | `'codecov-umbrella'` |
| `features`               | Space-separated list of features to enable during testing                     | No       | `''`                 |
| `no-default-features`    | Disable default features during testing                                       | No       | `false`              |
| `use-cross`              | Use cross-rs for testing. If false, use cargo.                                | No       | `false`              |
| `additional-test-args`   | Additional arguments to pass to the cargo test command                        | No       | `''`                 |

## Example Workflow

Here's an example workflow that uses this action with a matrix of configurations:

```yaml
name: Test and Coverage

on: [push]

jobs:
  test_and_coverage:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            use-cross: false
          - os: ubuntu-latest 
            target: i686-unknown-linux-gnu
            use-cross: false
          - os: ubuntu-latest
            target: aarch64-unknown-linux-gnu
            use-cross: true
          - os: ubuntu-latest
            target: armv7-unknown-linux-gnueabihf
            use-cross: true
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v2
      - name: Run Tests and Upload Coverage
        uses: Reloaded-Project/devops-rust-test-and-coverage@v1
        with:
          codecov-token: ${{ secrets.CODECOV_TOKEN }}
          features: 'feature1 feature2'
          no-default-features: true
          use-cross: ${{ matrix.use-cross }}
          use-tarpaulin: ${{ matrix.use-tarpaulin }}
          target: ${{ matrix.target }}
```

This workflow runs on every push and performs the following steps:
1. Checks out the repository
2. Runs the tests using `cargo` or `cross` based on the matrix configuration
3. Generates a coverage report using Tarpaulin (only when enabled and using `cargo`)
4. Uploads the coverage report to Codecov (only when Tarpaulin is enabled)

**Notes:** 
- Code coverage is skipped when using `cross`
- Tarpaulin can be disabled for platforms where it's unsupported
- When Tarpaulin is disabled, the action will only run tests without generating coverage reports

### Workflow for Binary Projects

This action is designed for Rust libraries without binary artifacts.

If you're working on a project with binary artifacts, consider using [devops-rust-lightweight-binary][rust-lw-binary],
instead, which will invoke this action as part of its workflow if tests are enabled.

## License

This GitHub Action is released under the [MIT License](LICENSE).

[rust-lw-binary]: https://github.com/Reloaded-Project/devops-rust-lightweight-binary