#[cfg(test)]
mod tests {
    use std::fs;
    use std::path::PathBuf;

    fn workspace_root() -> PathBuf {
        PathBuf::from(env!("CARGO_MANIFEST_DIR"))
            .parent()
            .expect("package directory should have a workspace root parent")
            .to_path_buf()
    }

    #[test]
    fn writes_marker() {
        fs::write(workspace_root().join("marker-package-c"), "ok\n").unwrap();
    }
}
