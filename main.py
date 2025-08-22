from app import download, convert, command_manager


def main():
    args = command_manager()
    if args.command == "download":
        download(args)
    elif args.command == "convert":
        convert(args)
    else:
        print("Command not found")
        args.print_help()


if __name__ == "__main__":
    main()
