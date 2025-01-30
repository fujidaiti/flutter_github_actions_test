import sys
import re


# バージョン番号のバリデーション
#
# - 期待するフォーマット : <major>.<minor>.<patch>+<build>
# - major, minor, patch, build はそれぞれ 0 以上の整数
# - +<build> は省略可能
# - 例: 1.2.3, 1.2.3+4
def validate_version(version: str) -> bool:
    pattern = r"^\d+\.\d+\.\d+(\+\d+)?$"
    if not re.match(pattern, version):
        raise ValueError(f"Invalid version format: {version}")
    return True


# バージョン番号をパースして整数のリストに変換
#
# - ビルド番号が省略されている場合は"+0"が指定されているものとして扱う
def parse_version(version: str) -> list:
    validate_version(version)
    if "+" not in version:
        version += "+0"
    return [int(x) for x in re.split(r"[\.\+]", version)]


# 2つのバージョン番号を比較
#
# - ビルド番号も比較対象とする
# - ビルド番号が省略されている場合は"+0"が指定されているものとして扱う
# - 返り値は以下の通り:
#   - version_a > version_b の場合は 1 を返す
#   - version_a < version_b の場合は -1 を返す
#   - version_a == version_b の場合は 0 を返す
# - 例:
#   - compare_versions("1.0.0", "1.1.0") => 1
#   - compare_versions("1.2.3+2", "1.2.3+1") => 1
#   - compare_versions("1.2.3", "2.0.0") => -1
#   - compare_versions("1.2.3", "1.2.3+0") => 0
def compare_versions(version_a: str, version_b: str) -> int:
    a_parts = parse_version(version_a)
    b_parts = parse_version(version_b)

    for a, b in zip(a_parts, b_parts):
        if a > b:
            return 1
        if a < b:
            return -1

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: compare_semver.py <version A> <version B>",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        result = compare_versions(sys.argv[1], sys.argv[2])
        print(result)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
