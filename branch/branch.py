from pathlib import Path
import argparse
import signal
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Display directory tree with file and directory limits.')
    parser.add_argument('directory', type=Path, nargs='?', default=Path('.'), help='Directory to list')
    parser.add_argument('-F', '--file-limit', type=int, default=10, help='Max number of files per directory')
    parser.add_argument('-D', '--dir-limit', type=int, default=10, help='Max number of directories per directory')
    return parser.parse_args()


def print_tree(path: Path, prefix: str, file_limit: int, dir_limit: int) -> None:
    try:
        entries = sorted(path.iterdir(), key=lambda e: (e.is_file(), e.name.lower()))
    except PermissionError:
        print(f"{prefix}└── [Permission Denied]")
        return

    directories = [e for e in entries if e.is_dir()]
    files = [e for e in entries if e.is_file()]

    displayed_dirs = directories[:dir_limit]
    remaining_dirs = len(directories) - dir_limit

    displayed_files = files[:file_limit]
    remaining_files = len(files) - file_limit

    all_displayed = displayed_dirs + displayed_files
    count = len(all_displayed)

    for index, entry in enumerate(all_displayed):
        connector = '├── ' if index < count - 1 else '└── '
        if entry.is_dir():
            print(f"{prefix}{connector}{entry.name}/")
            extension = '│   ' if index < count - 1 else '    '
            print_tree(entry, prefix + extension, file_limit, dir_limit)
        else:
            print(f"{prefix}{connector}{entry.name}")

    if remaining_dirs > 0:
        connector = '└── ' if count > 0 else ''
        print(f"{prefix}{connector}... [{remaining_dirs} more directories]")

    if remaining_files > 0:
        connector = '└── ' if count > 0 else ''
        print(f"{prefix}{connector}... [{remaining_files} more files]")


def main() -> None:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    try:
        args = parse_args()
        directory = args.directory.resolve()
        file_limit = args.file_limit
        dir_limit = args.dir_limit

        if not directory.is_dir():
            print(f"{directory} is not a directory.", file=sys.stderr)
            sys.exit(1)

        print(directory)
        print_tree(directory, '', file_limit, dir_limit)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(0)
    except BrokenPipeError:
        sys.exit(0)


if __name__ == '__main__':
    main()
