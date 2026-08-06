class UserProfile:
    def __init__(
        self,
        user_id,
        occupation=None,
        common_emotions=None,
        common_triggers=None,
        helpful_activities=None,
        unhelpful_activities=None,
        preferred_support_style=None
    ):
        self.user_id = user_id
        self.occupation = occupation
        self.common_emotions = common_emotions or []
        self.common_triggers = common_triggers or []
        self.helpful_activities = helpful_activities or []
        self.unhelpful_activities = unhelpful_activities or []
        self.preferred_support_style = preferred_support_style