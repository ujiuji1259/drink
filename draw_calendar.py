import calendar


cal = calendar.Calendar(firstweekday=6)
week = {0:'sun', 1:'mon', 2:'tue', 3:'wed', 4:'thu', 5:'fri', 6:'sat'}


def draw_calendar(year, month):
    html = ''
    days = list(cal.itermonthdates(year, month))

    for idx in range(0, len(days), 7):
        html += '<div class="fc-row fc-week fc-widget-content" style>\n'
        html += '<div class="fc-bg">\n'
        html += '<table class>\n'
        html += '<tbody>\n'
        html += '<tr>\n'

        for w, i in enumerate(days[idx:idx+7]):
            if i.month != month:
                html += '<td class="fc-day fc-widget-content fc-{0} fc-other-month fc-past" data-date="{1}"></td>\n'.format(week[w], str(i.year) + '-' + str(i.month) + '-' + str(i.day))
            else:
                html += '<td class="fc-day fc-widget-content fc-{0} fc-past" data-date="{1}"></td>\n'.format(week[w], str(i.year) + '-' + str(i.month) + '-' + str(i.day))

        html += '</tr>\n'
        html += '</tbody>\n'
        html += '</table>\n'
        html += '</div>\n'

        html += '<div class="fc-content-skeleton">\n'
        html += '<table>\n'
        html += '<thead>\n'
        html += '<tr>\n'

        for w, i in enumerate(days[idx:idx+7]):
            if i.month != month:
                html += '<td class="fc-day-top fc-{0} fc-other-month fc-past" data-date="{1}">\n'.format(week[w], str(i.year) + '-' + str(i.month) + '-' + str(i.day))
            else:
                html += '<td class="fc-day-top fc-{0} fc-past" data-date="{1}">\n'.format(week[w], str(i.year) + '-' + str(i.month) + '-' + str(i.day))

            html += '<span class="fc-day-number">' + str(i.day) + '</span>\n'
            html += '</td>\n'

        html += '</tr>\n'
        html += '</thead>\n'
        html += '<tbody>\n'
        html += '<tr>\n'

        for w, i in enumerate(days[idx:idx+7]):
            html += '<td></td>\n'
        html += '</tr>\n'
        html += '</tbody>\n'
        html += '</table>\n'
        html += '</div>\n'
        html += '</div>\n'

    return html

if __name__ == "__main__":
    print(draw_calendar(2020, 6))
