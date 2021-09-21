import uvicorn


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=11102, log_level="warning", fd=0)


if __name__ == "__main__":
    main()
