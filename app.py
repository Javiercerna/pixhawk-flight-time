from appJar import gui
from flight_time import createLogObject, computeFlightTime, formatSeconds

def processButton(button):
    if button == 'Process':
        log_filename = str(app.getEntry('Input_Log'))
        try:
            flight_time = computeFlightTime(createLogObject(log_filename))
            app.setLabel('Results', 'Flight time: ' + formatSeconds(flight_time))
        except TypeError as e:
            app.errorBox('Error', '\n'.join(e), parent=None)
    elif button == 'Quit':
        app.stop()

app = gui('Flight Time', useTtk=True)
app.setTtkTheme('vista')

app.addLabel('Choose log file')
app.addFileEntry('Input_Log')

app.addButtons(['Process', 'Quit'], processButton)

app.addEmptyLabel('Results')

app.go()
