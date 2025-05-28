from web_teamwork.hackathons.models import Hackathon, Participant


def resolve_hackathon_id_from_view(view):
    if hasattr(view, "get_hackathon_id"):
        return view.get_hackathon_id()
    return view.kwargs.get("hackathon_id")


def resolve_hackathon_id_from_obj(obj):
    match obj:
        case Hackathon():
            return obj.pk
        case Participant():
            return obj.hackathon_id
        case _:
            return None
