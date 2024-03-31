from techno_dominant.models import WeekdayModel


def create_weekdays(sender, **kwargs):
    if not WeekdayModel.objects.exists():
        weekday_names_index = [
            '0:Monday', '1:Tuesday', '2:Wednesday', '3:Thursday', 
            '4:Friday', '5:Saturday', '6:Sunday'
        ]
        for week in weekday_names_index:
            index, name = week.split(':')
            WeekdayModel.objects.create(index=index, name=name)

