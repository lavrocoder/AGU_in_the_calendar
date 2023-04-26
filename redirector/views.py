from django.shortcuts import redirect


def ical(request):
    type_param = request.GET.get('type', '')
    value_param = request.GET.get('value', 0)
    # Обработка параметров
    file_path = f"static/calendars/type_{type_param}_value_{value_param}.ics"
    return redirect(file_path)
