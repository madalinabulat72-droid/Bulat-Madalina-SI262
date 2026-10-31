from httptools import PATHS, report


def main():
    results = []

    for path in PATHS:
        result = report(path)
        result["path"] = path
        results.append(result)

    successful = [
        item for item in results
        if item["status"] == 200
    ]

    failed = [
        item for item in results
        if item["status"] != 200
    ]

    successful.sort(
        key=lambda item: item["seconds"],
        reverse=True
    )

    print("PAGINI REUȘITE:")

    for item in successful:
        print(
            item["path"],
            "->",
            item["status"],
            round(item["seconds"], 2),
            "secunde"
        )

    print()
    print("Reușite:", len(successful), "| Eșuate:", len(failed))


if __name__ == "__main__":
    main()