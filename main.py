import asyncio
from app import download, convert, command_manager


async def _async_main():
    """Internal async main function."""
    args = command_manager()
    if args.command == "download":
        await download(args)
    elif args.command == "convert":
        await convert(args)
    else:
        print("Command not found")
        args.print_help()


def main():
    """Main entry point for CLI that handles the async main function."""
    try:
        asyncio.run(_async_main())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Error: {e}")


# Keep cli_entry for backward compatibility
cli_entry = main


if __name__ == "__main__":
    main()
