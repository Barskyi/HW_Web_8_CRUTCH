import redis
from redis_lru import RedisLRU
from HW_Web_8_CRUTCH.HW_Web_8.models.models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_author(author: str) -> dict:
    # Find quotes by author's name
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


@cache
def find_by_tag(tag: str) -> list[str | None]:
    # Find quotes by tag
    quotes = Quote.objects(tags__icontains=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(tags: str) -> list[str | None]:
    tags_list = tags.split(',')
    result = set()
    for tag in tags_list:
        quotes = find_by_tag(tag)
        result.update(quotes)
    return list(result)


@cache
def print_all_tags():
    all_quotes = Quote.objects()
    all_tags = set()
    for quote in all_quotes:
        all_tags.update(quote.tags)
    return list(all_tags)


@cache
def print_all_authors():
    authors_list = []
    all_authors = Author.objects()
    for author in all_authors:
        authors_list.append(author.fullname)
    return authors_list


def request_db():
    message = ("How does it work!? You can write the full name or abbreviated.\nfor example -> "
               "name: Albert Einstein, tags: world or name: 'al', tags: 'wo'.\n"
               "If you want to view:\nThe authors name(press 1).\nTags(press 2).\n"
               "All available date (press 3).\n"
               "Back to menu (press 4).\n"
               "(or '0' to quit): ")
    print(message)
    while True:
        command = input()

        if command.isdigit():
            command = int(command)
            if command == 0:
                print("Have a nice day !")
                break
            elif command == 1:
                print("----------------------------------------------------------------")
                print(print_all_authors())
                print("----------------------------------------------------------------")
                print("Back to menu (press 4).")

            elif command == 2:
                print("----------------------------------------------------------------")
                print(print_all_tags())
                print("----------------------------------------------------------------")
                print("Back to menu (press 4).")

            elif command == 3:
                quotes = Quote.objects().all()
                print("----------------------------------------------------------------")
                print([e.to_json() for e in quotes])
                print("----------------------------------------------------------------")
                print("Back to menu (press 4).")

            elif command == 4:
                print("----------------------------------------------------------------")
                print(message)
                print("----------------------------------------------------------------")
            else:
                print("----------------------------------------------------------------")
                print("Invalid command. Please try again.")
                print("----------------------------------------------------------------")
                print("Back to menu (press 4).")

        else:
            parts = command.split(':')
            if len(parts) != 2:
                print("----------------------------------------------------------------")
                print("Invalid command format. Please try again.")
                print("----------------------------------------------------------------")
                print("Back to menu (press 4).")
                continue

            operation, value = parts[0].strip(), parts[1].strip()

            try:
                match operation:
                    case 'name':
                        quotes = find_by_author(value)
                        for author, quotes_list in quotes.items():
                            print("----------------------------------------------------------------")
                            print(f"Quotes by {author}:")
                            for quote in quotes_list:
                                print(f"- {quote}")
                                print("----------------------------------------------------------------")
                            print("Back to menu (press 4).")

                    case 'tag':
                        quotes = find_by_tag(value)
                        print("----------------------------------------------------------------")
                        print("Quotes for the tag:")
                        for quote in quotes:
                            print(f"- {quote}")
                            print("----------------------------------------------------------------")
                        print("Back to menu (press 4).")

                    case 'tags':
                        quotes = find_by_tags(value)
                        print("----------------------------------------------------------------")
                        print("Quotes for the tags:")
                        for quote in quotes:
                            print(f"- {quote}")
                            print("----------------------------------------------------------------")
                        print("Back to menu (press 4).")

                    case _:
                        # Check if the value matches the first two characters of any author name
                        matching_authors = [author for author in print_all_authors() if author[:2] == value[:2]]
                        if matching_authors:
                            print("----------------------------------------------------------------")
                            print("Matching authors:")
                            for author in matching_authors:
                                print(f"- {author}")
                                print("----------------------------------------------------------------")
                            print("Back to menu (press 4).")

                        else:
                            # If no authors found, search for quotes matching the tag
                            quotes = find_by_tag(value)
                            print("----------------------------------------------------------------")
                            print("Quotes for the tag or matching authors:")
                            for quote in quotes:
                                print(f"- {quote}")
                                print("----------------------------------------------------------------")
                            print("Back to menu (press 4).")

            except NameError:
                print("----------------------------------------------------------------")
                print("Unknown name. Please try again.")
                print("Back to menu (press 4).")


if __name__ == "__main__":
    """A script for searching for citations by tag, author's name or a set of tags"""
    request_db()
    # print(cache.get(""))
