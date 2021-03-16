from game import init, start
from settings import args


def main():
    init(
        strategy=args.strategy,
        used_map=args.map,
        ghosts_count=args.ghosts,
        is_campaign=args.campaign,
    )
    start()


if __name__ == '__main__':
    main()
