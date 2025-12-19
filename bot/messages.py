class Messages:
    """Main menu messages."""

    START_GREETING = "Hello {first_name}. How can I help you today?"

    # Category messages
    CATEGORY_EMPTY = (
        "You don't have any category! Try making a new one by tapping the button below."
    )
    CATEGORY_LIST_HEADER = "Here's are your categories:"
    CATEGORY_NAME_PROMPT = "Please write a name for the category."
    CATEGORY_CREATED = "Done"
    CATEGORY_NOT_FOUND = "Category not found."
    CATEGORY_VISIBILITY_UPDATED = "Category visibility updated."
    CATEGORY_DELETION_CONFIRM = "Are you sure you want to delete this category?"
    CATEGORY_DELETED = "Category deleted."

    # Category details
    CATEGORY_DETAIL = (
        "Editing Category:"
        "\n- Name: {name}"
        "\n- Visibility: {visibility}"
        "\n- Subscribers: {count}"
    )

    # Collection messages
    COLLECTION_EMPTY = "You don't have any collection! Try making a new one by tapping the button below."
    COLLECTION_LIST_HEADER = "Here's are your collections:"
    COLLECTION_NAME_PROMPT = "Please write a name for the collection."
    COLLECTION_CREATED = "Done"
    COLLECTION_NOT_FOUND = "Collection not found."

    # Visibility states
    VISIBILITY_PUBLIC = "Public"
    VISIBILITY_PRIVATE = "Private"


class ButtonTexts:
    """Button text labels."""

    # Main
    MAKE_FLASHCARD = "Make a Flashcard"
    BOOKMARKS = "Bookmarks"
    POPULAR_FLASHCARDS = "Popular Flashcards"

    # Navigation
    BACK = "🔙 Back"
    CREATE_CATEGORY = "+ Create a category"
    CREATE_COLLECTION = "+ Create a collection"

    # Visibility
    VISIBILITY_PUBLIC = "Public 🔓"
    VISIBILITY_PRIVATE = "Private 🔒"
    VISIBILITY_LABEL = "Visibility: {visibility}"

    # Actions
    DELETE_CATEGORY = "Delete Category ❌"
    CONFIRM = "Confirm"
    DELETE = "Delete"
    CANCEL = "Cancel"

    # Pagination
    FIRST_PAGE = "<<"
    PREVIOUS_PAGE = "<"
    NEXT_PAGE = ">"
    LAST_PAGE = ">>"
    SETTINGS = "⚙️"
