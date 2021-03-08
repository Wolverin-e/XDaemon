colors = {
    'cyan':             {'color': 'cyan'},
    'bright_cyan':      {'bright': True, 'color': 'cyan'},
    'bright_blue':      {'bright': True, 'color': 'blue'},
    'green':            {'color': 'green'},
    'yellow':           {'color': 'yellow'},
    'bold_yellow':      {'bold': True, 'color': 'yellow'},
    'magenta':          {'color': 'magenta'},
    'red':              {'color': 'red'},
    'bold_red':         {'bold': True, 'color': 'red'}
}

field_styles = {
    'name':             colors['bright_blue'],
    'funcName':         colors['bright_cyan'],
    'lineno':           colors['yellow'],
    'asctime':          colors['green'],
    'msecs':            colors['green'],
    'process':          colors['green'],
    'levelname':        colors['bold_yellow'],
    'levelno':          colors['bold_yellow'],
}

level_styles = {
    'debug':            colors['bright_cyan'],
    'info':             colors['bright_blue'],
    'warning':          colors['yellow'],
    'error':            colors['red'],
    'critical':         colors['bold_red'],
}
