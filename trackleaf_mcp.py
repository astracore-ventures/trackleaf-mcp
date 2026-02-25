from trackleaf_mcp_pkg.runner import main


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        import sys

        print(f"[trackleaf-cursor-mcp] fatal: {e}", file=sys.stderr)
        raise