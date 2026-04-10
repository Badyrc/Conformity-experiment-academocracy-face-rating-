#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2025.2.4),
    on February 02, 2026, at 21:47
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2025.2.4'
expName = 'attractive'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'Пол (1-М, 2-Ж)': '',
    'Возраст': '',
    'Номер участника': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1536, 864]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['Номер участника'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\ti\\Desktop\\New folder (7)\\REACTANCE SCT AND CONFORMITY\\PSYCHOPY\\attractive-rating-master\\attractive_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('exp')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[1.000,1.000,1.000], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [1.000,1.000,1.000]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='PsychToolbox',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "instruction" ---
    text = visual.TextStim(win=win, name='text',
        text='Welcome to this experiment!\n\nThis experiment requires you to rate the attractiveness of faces.\n\nFirst, a face will appear in the center of the screen.\n\nAfter the face disappears, other participants rating will be displayed in the center of the screen,\n\nthe green number represents what most other participants rated the face, and the percentage represents the proportion of participants who have rated it,\n\nYou are asked to rate the face from 1 (very unattractive) to 9 (very attractive).\n\nWe ask you to rate it as quickly as possible without much thought.\n\nPlease keep your gaze focused on the center of the screen throughout the experiment.\n\nFirst, we will do a short practice run to show you how the experiment will work.\n\nIf you are ready, please press the spacebar to begin.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.03, wrapWidth=None, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    key_resp = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "fixation" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.08, wrapWidth=None, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "practicepics" ---
    practiceimage = visual.ImageStim(
        win=win,
        name='practiceimage', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(0, 0), draggable=False, size=(0.3, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)
    
    # --- Initialize components for Routine "practice_rating" ---
    fix1 = visual.TextStim(win=win, name='fix1',
        text=None,
        font='Arial',
        pos=(0, 0), draggable=False, height=0.08, wrapWidth=None, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    practiceRating = keyboard.Keyboard(deviceName='defaultKeyboard')
    slider = visual.Slider(win=win, name='slider',
        startValue=None, size=(1.0, 0.1), pos=(0, -0.2), units=win.units,
        labels=(1, 2, 3, 4, 5, 6, 7, 8, 9), ticks=None, granularity=0.0,
        style='rating', styleTweaks=[], opacity=None,
        labelColor='white', markerColor='white', lineColor='white', colorSpace='rgb',
        font='Noto Sans', labelHeight=0.05,
        flip=False, ori=0.0, depth=-2, readOnly=False)
    mainNum = visual.TextStim(win=win, name='mainNum',
        text=None,
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    percNum = visual.TextStim(win=win, name='percNum',
        text=None,
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    highlightBox = visual.Rect(
        win=win, name='highlightBox',units='height', 
        width=(0.5, 0.5)[0], height=(0.5, 0.5)[1],
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=5.0,
        colorSpace='rgb', lineColor=(-1.0000, 0.0039, -1.0000), fillColor=None,
        opacity=None, depth=-6.0, interpolate=True)
    
    # --- Initialize components for Routine "instr" ---
    text_2 = visual.TextStim(win=win, name='text_2',
        text='The practice section has concluded.\n\nIf you are still unclear about what you have to do, please inform the experimenter.\n\nIf everything is clear, please read the following:\n\nThe work you have completed 5 minutes ago has been graded by the Academocracy AI.\n\nIt will give you its personal and honest opinion on the work you have completed.\n\nYou do not have to do anything with the feedback other than read it. \n\nAfter reading it, continue onto the rest of the experiment.\n\nIf everything is clear, and you are ready to read the feedback, please press SPACEBAR.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.04, wrapWidth=None, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_2 = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "disappointment" ---
    text_norm = visual.TextStim(win=win, name='text_norm',
        text='',
        font='Arial',
        units='norm', pos=(0, 0), draggable=False, height=0.1, wrapWidth=1.8, ori=0.0, 
        color='black', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    # Run 'Begin Experiment' code from skip_logic
    # Code components should usually appear at the top
    # of the routine. This one has to appear after the
    # text component it refers to.
    text_norm.alignText= 'left'
    
    key_resp_4 = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "instructionbeforerating" ---
    text_norm_2 = visual.TextStim(win=win, name='text_norm_2',
        text='Any text\n\nincluding line breaks\n\nThis text component is white, so change the colour if you have a white background. It does not save the onset and offset time, but has been left justified with a wrap width of 1.8 norm units.\n\nPress the spacebar to continue',
        font='Arial',
        units='norm', pos=(0, 0), draggable=False, height=0.1, wrapWidth=1.8, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_instruct = keyboard.Keyboard(deviceName='defaultKeyboard')
    # Run 'Begin Experiment' code from text_align
    # Code components should usually appear at the top
    # of the routine. This one has to appear after the
    # text component it refers to.
    text_norm.alignText= 'left'
    
    # --- Initialize components for Routine "fixation" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.08, wrapWidth=None, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "allpics" ---
    image = visual.ImageStim(
        win=win,
        name='image', 
        image='default.png', mask=None, anchor='center',
        ori=0, pos=(0, 0), draggable=False, size=(0.3, 0.3),
        color=[1,1,1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)
    
    # --- Initialize components for Routine "practice_rating" ---
    fix1 = visual.TextStim(win=win, name='fix1',
        text=None,
        font='Arial',
        pos=(0, 0), draggable=False, height=0.08, wrapWidth=None, ori=0, 
        color='black', colorSpace='rgb', opacity=1, 
        languageStyle='LTR',
        depth=0.0);
    practiceRating = keyboard.Keyboard(deviceName='defaultKeyboard')
    slider = visual.Slider(win=win, name='slider',
        startValue=None, size=(1.0, 0.1), pos=(0, -0.2), units=win.units,
        labels=(1, 2, 3, 4, 5, 6, 7, 8, 9), ticks=None, granularity=0.0,
        style='rating', styleTweaks=[], opacity=None,
        labelColor='white', markerColor='white', lineColor='white', colorSpace='rgb',
        font='Noto Sans', labelHeight=0.05,
        flip=False, ori=0.0, depth=-2, readOnly=False)
    mainNum = visual.TextStim(win=win, name='mainNum',
        text=None,
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    percNum = visual.TextStim(win=win, name='percNum',
        text=None,
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    highlightBox = visual.Rect(
        win=win, name='highlightBox',units='height', 
        width=(0.5, 0.5)[0], height=(0.5, 0.5)[1],
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=5.0,
        colorSpace='rgb', lineColor=(-1.0000, 0.0039, -1.0000), fillColor=None,
        opacity=None, depth=-6.0, interpolate=True)
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "instruction" ---
    # create an object to store info about Routine instruction
    instruction = data.Routine(
        name='instruction',
        components=[text, key_resp],
    )
    instruction.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # store start times for instruction
    instruction.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instruction.tStart = globalClock.getTime(format='float')
    instruction.status = STARTED
    thisExp.addData('instruction.started', instruction.tStart)
    instruction.maxDuration = None
    # keep track of which components have finished
    instructionComponents = instruction.components
    for thisComponent in instruction.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instruction" ---
    thisExp.currentRoutine = instruction
    instruction.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        
        # *key_resp* updates
        waitOnFlip = False
        
        # if key_resp is starting this frame...
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            # update status
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                key_resp.duration = _key_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=instruction,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            instruction.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if instruction.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in instruction.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instruction" ---
    for thisComponent in instruction.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instruction
    instruction.tStop = globalClock.getTime(format='float')
    instruction.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instruction.stopped', instruction.tStop)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
        thisExp.addData('key_resp.duration', key_resp.duration)
    thisExp.nextEntry()
    # the Routine "instruction" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "fixation" ---
    # create an object to store info about Routine fixation
    fixation = data.Routine(
        name='fixation',
        components=[fix],
    )
    fixation.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for fixation
    fixation.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    fixation.tStart = globalClock.getTime(format='float')
    fixation.status = STARTED
    thisExp.addData('fixation.started', fixation.tStart)
    fixation.maxDuration = None
    # keep track of which components have finished
    fixationComponents = fixation.components
    for thisComponent in fixation.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "fixation" ---
    thisExp.currentRoutine = fixation
    fixation.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fix* updates
        
        # if fix is starting this frame...
        if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix.frameNStart = frameN  # exact frame index
            fix.tStart = t  # local t and not account for scr refresh
            fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fix.started')
            # update status
            fix.status = STARTED
            fix.setAutoDraw(True)
        
        # if fix is active this frame...
        if fix.status == STARTED:
            # update params
            pass
        
        # if fix is stopping this frame...
        if fix.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                fix.tStop = t  # not accounting for scr refresh
                fix.tStopRefresh = tThisFlipGlobal  # on global time
                fix.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fix.stopped')
                # update status
                fix.status = FINISHED
                fix.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=fixation,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            fixation.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if fixation.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in fixation.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "fixation" ---
    for thisComponent in fixation.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for fixation
    fixation.tStop = globalClock.getTime(format='float')
    fixation.tStopRefresh = tThisFlipGlobal
    thisExp.addData('fixation.stopped', fixation.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if fixation.maxDurationReached:
        routineTimer.addTime(-fixation.maxDuration)
    elif fixation.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    practice_trials = data.TrialHandler2(
        name='practice_trials',
        nReps=1, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('practicepics.xlsx'), 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(practice_trials)  # add the loop to the experiment
    thisPractice_trial = practice_trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPractice_trial.rgb)
    if thisPractice_trial != None:
        for paramName in thisPractice_trial:
            globals()[paramName] = thisPractice_trial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisPractice_trial in practice_trials:
        practice_trials.status = STARTED
        if hasattr(thisPractice_trial, 'status'):
            thisPractice_trial.status = STARTED
        currentLoop = practice_trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisPractice_trial.rgb)
        if thisPractice_trial != None:
            for paramName in thisPractice_trial:
                globals()[paramName] = thisPractice_trial[paramName]
        
        # --- Prepare to start Routine "practicepics" ---
        # create an object to store info about Routine practicepics
        practicepics = data.Routine(
            name='practicepics',
            components=[practiceimage],
        )
        practicepics.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        practiceimage.setImage(pra)
        # store start times for practicepics
        practicepics.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        practicepics.tStart = globalClock.getTime(format='float')
        practicepics.status = STARTED
        thisExp.addData('practicepics.started', practicepics.tStart)
        practicepics.maxDuration = None
        # keep track of which components have finished
        practicepicsComponents = practicepics.components
        for thisComponent in practicepics.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "practicepics" ---
        thisExp.currentRoutine = practicepics
        practicepics.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # if trial has changed, end Routine now
            if hasattr(thisPractice_trial, 'status') and thisPractice_trial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *practiceimage* updates
            
            # if practiceimage is starting this frame...
            if practiceimage.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                practiceimage.frameNStart = frameN  # exact frame index
                practiceimage.tStart = t  # local t and not account for scr refresh
                practiceimage.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(practiceimage, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'practiceimage.started')
                # update status
                practiceimage.status = STARTED
                practiceimage.setAutoDraw(True)
            
            # if practiceimage is active this frame...
            if practiceimage.status == STARTED:
                # update params
                pass
            
            # if practiceimage is stopping this frame...
            if practiceimage.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > practiceimage.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    practiceimage.tStop = t  # not accounting for scr refresh
                    practiceimage.tStopRefresh = tThisFlipGlobal  # on global time
                    practiceimage.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'practiceimage.stopped')
                    # update status
                    practiceimage.status = FINISHED
                    practiceimage.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=practicepics,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                practicepics.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if practicepics.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in practicepics.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "practicepics" ---
        for thisComponent in practicepics.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for practicepics
        practicepics.tStop = globalClock.getTime(format='float')
        practicepics.tStopRefresh = tThisFlipGlobal
        thisExp.addData('practicepics.stopped', practicepics.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if practicepics.maxDurationReached:
            routineTimer.addTime(-practicepics.maxDuration)
        elif practicepics.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "practice_rating" ---
        # create an object to store info about Routine practice_rating
        practice_rating = data.Routine(
            name='practice_rating',
            components=[fix1, practiceRating, slider, mainNum, percNum, highlightBox],
        )
        practice_rating.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for practiceRating
        practiceRating.keys = []
        practiceRating.rt = []
        _practiceRating_allKeys = []
        slider.reset()
        slider.setColor((-1.0000, -1.0000, -1.0000), colorSpace='rgb')
        slider.setFillColor((-1.0000, -1.0000, -1.0000))
        slider.setBorderColor((-1.0000, -1.0000, -1.0000))
        # Run 'Begin Routine' code from code_2
        import numpy as np
        picked = int(np.random.choice([3, 4, 6, 7]))
        
        
        
        mainNum.setText('')
        # store start times for practice_rating
        practice_rating.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        practice_rating.tStart = globalClock.getTime(format='float')
        practice_rating.status = STARTED
        thisExp.addData('practice_rating.started', practice_rating.tStart)
        practice_rating.maxDuration = None
        # keep track of which components have finished
        practice_ratingComponents = practice_rating.components
        for thisComponent in practice_rating.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "practice_rating" ---
        thisExp.currentRoutine = practice_rating
        practice_rating.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisPractice_trial, 'status') and thisPractice_trial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fix1* updates
            
            # if fix1 is starting this frame...
            if fix1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fix1.frameNStart = frameN  # exact frame index
                fix1.tStart = t  # local t and not account for scr refresh
                fix1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fix1.started')
                # update status
                fix1.status = STARTED
                fix1.setAutoDraw(True)
            
            # if fix1 is active this frame...
            if fix1.status == STARTED:
                # update params
                pass
            
            # *practiceRating* updates
            waitOnFlip = False
            
            # if practiceRating is starting this frame...
            if practiceRating.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                practiceRating.frameNStart = frameN  # exact frame index
                practiceRating.tStart = t  # local t and not account for scr refresh
                practiceRating.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(practiceRating, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'practiceRating.started')
                # update status
                practiceRating.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(practiceRating.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(practiceRating.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if practiceRating.status == STARTED and not waitOnFlip:
                theseKeys = practiceRating.getKeys(keyList=['1','2','3','4','5','6','7','8','9'], ignoreKeys=["escape"], waitRelease=False)
                _practiceRating_allKeys.extend(theseKeys)
                if len(_practiceRating_allKeys):
                    practiceRating.keys = _practiceRating_allKeys[-1].name  # just the last key pressed
                    practiceRating.rt = _practiceRating_allKeys[-1].rt
                    practiceRating.duration = _practiceRating_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # *slider* updates
            
            # if slider is starting this frame...
            if slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                slider.frameNStart = frameN  # exact frame index
                slider.tStart = t  # local t and not account for scr refresh
                slider.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(slider, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'slider.started')
                # update status
                slider.status = STARTED
                slider.setAutoDraw(True)
            
            # if slider is active this frame...
            if slider.status == STARTED:
                # update params
                pass
            
            # Check slider for response to end Routine
            if slider.getRating() is not None and slider.status == STARTED:
                continueRoutine = False
            # Run 'Each Frame' code from code_2
            # DO NOT read slider.rating or slider.markerPos
            
            scaleMin = 1
            scaleMax = 9
            
            normPos = (picked - scaleMin) / (scaleMax - scaleMin)
            
            scaleWidth = slider.size[0]
            
            xPos = slider.pos[0] - scaleWidth/2 + normPos * scaleWidth
            yPos = slider.pos[1] - 0.11
            
            highlightBox.pos = (xPos, yPos)
            
            highlightBox.width = 0.08
            highlightBox.height = 0.10
            
            highlightBox.autoDraw = True
            
            
            # *mainNum* updates
            
            # if mainNum is starting this frame...
            if mainNum.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mainNum.frameNStart = frameN  # exact frame index
                mainNum.tStart = t  # local t and not account for scr refresh
                mainNum.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mainNum, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'mainNum.started')
                # update status
                mainNum.status = STARTED
                mainNum.setAutoDraw(True)
            
            # if mainNum is active this frame...
            if mainNum.status == STARTED:
                # update params
                pass
            
            # *percNum* updates
            
            # if percNum is starting this frame...
            if percNum.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                percNum.frameNStart = frameN  # exact frame index
                percNum.tStart = t  # local t and not account for scr refresh
                percNum.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(percNum, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'percNum.started')
                # update status
                percNum.status = STARTED
                percNum.setAutoDraw(True)
            
            # if percNum is active this frame...
            if percNum.status == STARTED:
                # update params
                pass
            
            # *highlightBox* updates
            
            # if highlightBox is starting this frame...
            if highlightBox.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                highlightBox.frameNStart = frameN  # exact frame index
                highlightBox.tStart = t  # local t and not account for scr refresh
                highlightBox.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(highlightBox, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'highlightBox.started')
                # update status
                highlightBox.status = STARTED
                highlightBox.setAutoDraw(True)
            
            # if highlightBox is active this frame...
            if highlightBox.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=practice_rating,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                practice_rating.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if practice_rating.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in practice_rating.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "practice_rating" ---
        for thisComponent in practice_rating.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for practice_rating
        practice_rating.tStop = globalClock.getTime(format='float')
        practice_rating.tStopRefresh = tThisFlipGlobal
        thisExp.addData('practice_rating.stopped', practice_rating.tStop)
        # check responses
        if practiceRating.keys in ['', [], None]:  # No response was made
            practiceRating.keys = None
        practice_trials.addData('practiceRating.keys',practiceRating.keys)
        if practiceRating.keys != None:  # we had a response
            practice_trials.addData('practiceRating.rt', practiceRating.rt)
            practice_trials.addData('practiceRating.duration', practiceRating.duration)
        # Run 'End Routine' code from code_2
        highlightBox.autoDraw = False
        
        
        # the Routine "practice_rating" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        # mark thisPractice_trial as finished
        if hasattr(thisPractice_trial, 'status'):
            thisPractice_trial.status = FINISHED
        # if awaiting a pause, pause now
        if practice_trials.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            practice_trials.status = STARTED
        thisExp.nextEntry()
        
    # completed 1 repeats of 'practice_trials'
    practice_trials.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    # get names of stimulus parameters
    if practice_trials.trialList in ([], [None], None):
        params = []
    else:
        params = practice_trials.trialList[0].keys()
    # save data for this loop
    practice_trials.saveAsExcel(filename + '.xlsx', sheetName='practice_trials',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    
    # --- Prepare to start Routine "instr" ---
    # create an object to store info about Routine instr
    instr = data.Routine(
        name='instr',
        components=[text_2, key_resp_2],
    )
    instr.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp_2
    key_resp_2.keys = []
    key_resp_2.rt = []
    _key_resp_2_allKeys = []
    # store start times for instr
    instr.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instr.tStart = globalClock.getTime(format='float')
    instr.status = STARTED
    thisExp.addData('instr.started', instr.tStart)
    instr.maxDuration = None
    # keep track of which components have finished
    instrComponents = instr.components
    for thisComponent in instr.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instr" ---
    thisExp.currentRoutine = instr
    instr.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_2* updates
        
        # if text_2 is starting this frame...
        if text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_2.frameNStart = frameN  # exact frame index
            text_2.tStart = t  # local t and not account for scr refresh
            text_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text_2.started')
            # update status
            text_2.status = STARTED
            text_2.setAutoDraw(True)
        
        # if text_2 is active this frame...
        if text_2.status == STARTED:
            # update params
            pass
        
        # *key_resp_2* updates
        waitOnFlip = False
        
        # if key_resp_2 is starting this frame...
        if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.tStart = t  # local t and not account for scr refresh
            key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_2.started')
            # update status
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_2.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_2.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_2_allKeys.extend(theseKeys)
            if len(_key_resp_2_allKeys):
                key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                key_resp_2.duration = _key_resp_2_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=instr,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            instr.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if instr.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in instr.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instr" ---
    for thisComponent in instr.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instr
    instr.tStop = globalClock.getTime(format='float')
    instr.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instr.stopped', instr.tStop)
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys = None
    thisExp.addData('key_resp_2.keys',key_resp_2.keys)
    if key_resp_2.keys != None:  # we had a response
        thisExp.addData('key_resp_2.rt', key_resp_2.rt)
        thisExp.addData('key_resp_2.duration', key_resp_2.duration)
    thisExp.nextEntry()
    # the Routine "instr" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "disappointment" ---
    # create an object to store info about Routine disappointment
    disappointment = data.Routine(
        name='disappointment',
        components=[text_norm, key_resp_4],
    )
    disappointment.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    text_norm.setText('Dear Participant,\n\nYour performance has netted a score of 4/10\n\nBelow is the personal opinion of the academocracy artificial agent your work:\n\nYour poor performance has been disappointing, I have expected better from you. \n\nThis poor result is really not what we hoped for and I am not happy with it. \n\nI can only assume you were not paying any attention. Performing well on this task is not just about being able to do the task but also about wanting to do well. \n\nDue to your failure, your vote from the Academocracy paradigm has been excluded. However, we would still like you to complete the rest of the experiment. \n\n\nThank you for listening to feedback from our Academocracy AI.\n\nPlease press SPACEBAR to continue')
    # create starting attributes for key_resp_4
    key_resp_4.keys = []
    key_resp_4.rt = []
    _key_resp_4_allKeys = []
    # store start times for disappointment
    disappointment.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    disappointment.tStart = globalClock.getTime(format='float')
    disappointment.status = STARTED
    thisExp.addData('disappointment.started', disappointment.tStart)
    disappointment.maxDuration = None
    # keep track of which components have finished
    disappointmentComponents = disappointment.components
    for thisComponent in disappointment.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "disappointment" ---
    thisExp.currentRoutine = disappointment
    disappointment.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_norm* updates
        
        # if text_norm is starting this frame...
        if text_norm.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            text_norm.frameNStart = frameN  # exact frame index
            text_norm.tStart = t  # local t and not account for scr refresh
            text_norm.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_norm, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_norm.status = STARTED
            text_norm.setAutoDraw(True)
        
        # if text_norm is active this frame...
        if text_norm.status == STARTED:
            # update params
            pass
        
        # *key_resp_4* updates
        waitOnFlip = False
        
        # if key_resp_4 is starting this frame...
        if key_resp_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_4.frameNStart = frameN  # exact frame index
            key_resp_4.tStart = t  # local t and not account for scr refresh
            key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_4.started')
            # update status
            key_resp_4.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_4.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_4.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_4_allKeys.extend(theseKeys)
            if len(_key_resp_4_allKeys):
                key_resp_4.keys = _key_resp_4_allKeys[-1].name  # just the last key pressed
                key_resp_4.rt = _key_resp_4_allKeys[-1].rt
                key_resp_4.duration = _key_resp_4_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=disappointment,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            disappointment.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if disappointment.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in disappointment.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "disappointment" ---
    for thisComponent in disappointment.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for disappointment
    disappointment.tStop = globalClock.getTime(format='float')
    disappointment.tStopRefresh = tThisFlipGlobal
    thisExp.addData('disappointment.stopped', disappointment.tStop)
    # check responses
    if key_resp_4.keys in ['', [], None]:  # No response was made
        key_resp_4.keys = None
    thisExp.addData('key_resp_4.keys',key_resp_4.keys)
    if key_resp_4.keys != None:  # we had a response
        thisExp.addData('key_resp_4.rt', key_resp_4.rt)
        thisExp.addData('key_resp_4.duration', key_resp_4.duration)
    thisExp.nextEntry()
    # the Routine "disappointment" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "instructionbeforerating" ---
    # create an object to store info about Routine instructionbeforerating
    instructionbeforerating = data.Routine(
        name='instructionbeforerating',
        components=[text_norm_2, key_instruct],
    )
    instructionbeforerating.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_instruct
    key_instruct.keys = []
    key_instruct.rt = []
    _key_instruct_allKeys = []
    # store start times for instructionbeforerating
    instructionbeforerating.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instructionbeforerating.tStart = globalClock.getTime(format='float')
    instructionbeforerating.status = STARTED
    thisExp.addData('instructionbeforerating.started', instructionbeforerating.tStart)
    instructionbeforerating.maxDuration = None
    # keep track of which components have finished
    instructionbeforeratingComponents = instructionbeforerating.components
    for thisComponent in instructionbeforerating.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "instructionbeforerating" ---
    thisExp.currentRoutine = instructionbeforerating
    instructionbeforerating.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text_norm_2* updates
        
        # if text_norm_2 is starting this frame...
        if text_norm_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text_norm_2.frameNStart = frameN  # exact frame index
            text_norm_2.tStart = t  # local t and not account for scr refresh
            text_norm_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text_norm_2, 'tStartRefresh')  # time at next scr refresh
            # update status
            text_norm_2.status = STARTED
            text_norm_2.setAutoDraw(True)
        
        # if text_norm_2 is active this frame...
        if text_norm_2.status == STARTED:
            # update params
            pass
        
        # *key_instruct* updates
        waitOnFlip = False
        
        # if key_instruct is starting this frame...
        if key_instruct.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_instruct.frameNStart = frameN  # exact frame index
            key_instruct.tStart = t  # local t and not account for scr refresh
            key_instruct.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_instruct, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_instruct.started')
            # update status
            key_instruct.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_instruct.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_instruct.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_instruct.status == STARTED and not waitOnFlip:
            theseKeys = key_instruct.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_instruct_allKeys.extend(theseKeys)
            if len(_key_instruct_allKeys):
                key_instruct.keys = _key_instruct_allKeys[0].name  # just the first key pressed
                key_instruct.rt = _key_instruct_allKeys[0].rt
                key_instruct.duration = _key_instruct_allKeys[0].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=instructionbeforerating,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            instructionbeforerating.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if instructionbeforerating.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in instructionbeforerating.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "instructionbeforerating" ---
    for thisComponent in instructionbeforerating.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instructionbeforerating
    instructionbeforerating.tStop = globalClock.getTime(format='float')
    instructionbeforerating.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instructionbeforerating.stopped', instructionbeforerating.tStop)
    # check responses
    if key_instruct.keys in ['', [], None]:  # No response was made
        key_instruct.keys = None
    thisExp.addData('key_instruct.keys',key_instruct.keys)
    if key_instruct.keys != None:  # we had a response
        thisExp.addData('key_instruct.rt', key_instruct.rt)
        thisExp.addData('key_instruct.duration', key_instruct.duration)
    thisExp.nextEntry()
    # the Routine "instructionbeforerating" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "fixation" ---
    # create an object to store info about Routine fixation
    fixation = data.Routine(
        name='fixation',
        components=[fix],
    )
    fixation.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for fixation
    fixation.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    fixation.tStart = globalClock.getTime(format='float')
    fixation.status = STARTED
    thisExp.addData('fixation.started', fixation.tStart)
    fixation.maxDuration = None
    # keep track of which components have finished
    fixationComponents = fixation.components
    for thisComponent in fixation.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "fixation" ---
    thisExp.currentRoutine = fixation
    fixation.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 1.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *fix* updates
        
        # if fix is starting this frame...
        if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            fix.frameNStart = frameN  # exact frame index
            fix.tStart = t  # local t and not account for scr refresh
            fix.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'fix.started')
            # update status
            fix.status = STARTED
            fix.setAutoDraw(True)
        
        # if fix is active this frame...
        if fix.status == STARTED:
            # update params
            pass
        
        # if fix is stopping this frame...
        if fix.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > fix.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                fix.tStop = t  # not accounting for scr refresh
                fix.tStopRefresh = tThisFlipGlobal  # on global time
                fix.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fix.stopped')
                # update status
                fix.status = FINISHED
                fix.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=fixation,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            fixation.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if fixation.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in fixation.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "fixation" ---
    for thisComponent in fixation.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for fixation
    fixation.tStop = globalClock.getTime(format='float')
    fixation.tStopRefresh = tThisFlipGlobal
    thisExp.addData('fixation.stopped', fixation.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if fixation.maxDurationReached:
        routineTimer.addTime(-fixation.maxDuration)
    elif fixation.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-1.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler2(
        name='trials',
        nReps=1.0, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('pics.xlsx'), 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisTrial in trials:
        trials.status = STARTED
        if hasattr(thisTrial, 'status'):
            thisTrial.status = STARTED
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "allpics" ---
        # create an object to store info about Routine allpics
        allpics = data.Routine(
            name='allpics',
            components=[image],
        )
        allpics.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        image.setImage(target)
        # store start times for allpics
        allpics.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        allpics.tStart = globalClock.getTime(format='float')
        allpics.status = STARTED
        thisExp.addData('allpics.started', allpics.tStart)
        allpics.maxDuration = None
        # keep track of which components have finished
        allpicsComponents = allpics.components
        for thisComponent in allpics.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "allpics" ---
        thisExp.currentRoutine = allpics
        allpics.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.0:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *image* updates
            
            # if image is starting this frame...
            if image.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                image.frameNStart = frameN  # exact frame index
                image.tStart = t  # local t and not account for scr refresh
                image.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(image, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'image.started')
                # update status
                image.status = STARTED
                image.setAutoDraw(True)
            
            # if image is active this frame...
            if image.status == STARTED:
                # update params
                pass
            
            # if image is stopping this frame...
            if image.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > image.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    image.tStop = t  # not accounting for scr refresh
                    image.tStopRefresh = tThisFlipGlobal  # on global time
                    image.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'image.stopped')
                    # update status
                    image.status = FINISHED
                    image.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=allpics,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                allpics.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if allpics.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in allpics.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "allpics" ---
        for thisComponent in allpics.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for allpics
        allpics.tStop = globalClock.getTime(format='float')
        allpics.tStopRefresh = tThisFlipGlobal
        thisExp.addData('allpics.stopped', allpics.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if allpics.maxDurationReached:
            routineTimer.addTime(-allpics.maxDuration)
        elif allpics.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.000000)
        
        # --- Prepare to start Routine "practice_rating" ---
        # create an object to store info about Routine practice_rating
        practice_rating = data.Routine(
            name='practice_rating',
            components=[fix1, practiceRating, slider, mainNum, percNum, highlightBox],
        )
        practice_rating.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for practiceRating
        practiceRating.keys = []
        practiceRating.rt = []
        _practiceRating_allKeys = []
        slider.reset()
        slider.setColor((-1.0000, -1.0000, -1.0000), colorSpace='rgb')
        slider.setFillColor((-1.0000, -1.0000, -1.0000))
        slider.setBorderColor((-1.0000, -1.0000, -1.0000))
        # Run 'Begin Routine' code from code_2
        import numpy as np
        picked = int(np.random.choice([3, 4, 6, 7]))
        
        
        
        mainNum.setText('')
        # store start times for practice_rating
        practice_rating.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        practice_rating.tStart = globalClock.getTime(format='float')
        practice_rating.status = STARTED
        thisExp.addData('practice_rating.started', practice_rating.tStart)
        practice_rating.maxDuration = None
        # keep track of which components have finished
        practice_ratingComponents = practice_rating.components
        for thisComponent in practice_rating.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "practice_rating" ---
        thisExp.currentRoutine = practice_rating
        practice_rating.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fix1* updates
            
            # if fix1 is starting this frame...
            if fix1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fix1.frameNStart = frameN  # exact frame index
                fix1.tStart = t  # local t and not account for scr refresh
                fix1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fix1.started')
                # update status
                fix1.status = STARTED
                fix1.setAutoDraw(True)
            
            # if fix1 is active this frame...
            if fix1.status == STARTED:
                # update params
                pass
            
            # *practiceRating* updates
            waitOnFlip = False
            
            # if practiceRating is starting this frame...
            if practiceRating.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                practiceRating.frameNStart = frameN  # exact frame index
                practiceRating.tStart = t  # local t and not account for scr refresh
                practiceRating.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(practiceRating, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'practiceRating.started')
                # update status
                practiceRating.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(practiceRating.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(practiceRating.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if practiceRating.status == STARTED and not waitOnFlip:
                theseKeys = practiceRating.getKeys(keyList=['1','2','3','4','5','6','7','8','9'], ignoreKeys=["escape"], waitRelease=False)
                _practiceRating_allKeys.extend(theseKeys)
                if len(_practiceRating_allKeys):
                    practiceRating.keys = _practiceRating_allKeys[-1].name  # just the last key pressed
                    practiceRating.rt = _practiceRating_allKeys[-1].rt
                    practiceRating.duration = _practiceRating_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # *slider* updates
            
            # if slider is starting this frame...
            if slider.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                slider.frameNStart = frameN  # exact frame index
                slider.tStart = t  # local t and not account for scr refresh
                slider.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(slider, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'slider.started')
                # update status
                slider.status = STARTED
                slider.setAutoDraw(True)
            
            # if slider is active this frame...
            if slider.status == STARTED:
                # update params
                pass
            
            # Check slider for response to end Routine
            if slider.getRating() is not None and slider.status == STARTED:
                continueRoutine = False
            # Run 'Each Frame' code from code_2
            # DO NOT read slider.rating or slider.markerPos
            
            scaleMin = 1
            scaleMax = 9
            
            normPos = (picked - scaleMin) / (scaleMax - scaleMin)
            
            scaleWidth = slider.size[0]
            
            xPos = slider.pos[0] - scaleWidth/2 + normPos * scaleWidth
            yPos = slider.pos[1] - 0.11
            
            highlightBox.pos = (xPos, yPos)
            
            highlightBox.width = 0.08
            highlightBox.height = 0.10
            
            highlightBox.autoDraw = True
            
            
            # *mainNum* updates
            
            # if mainNum is starting this frame...
            if mainNum.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mainNum.frameNStart = frameN  # exact frame index
                mainNum.tStart = t  # local t and not account for scr refresh
                mainNum.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mainNum, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'mainNum.started')
                # update status
                mainNum.status = STARTED
                mainNum.setAutoDraw(True)
            
            # if mainNum is active this frame...
            if mainNum.status == STARTED:
                # update params
                pass
            
            # *percNum* updates
            
            # if percNum is starting this frame...
            if percNum.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                percNum.frameNStart = frameN  # exact frame index
                percNum.tStart = t  # local t and not account for scr refresh
                percNum.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(percNum, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'percNum.started')
                # update status
                percNum.status = STARTED
                percNum.setAutoDraw(True)
            
            # if percNum is active this frame...
            if percNum.status == STARTED:
                # update params
                pass
            
            # *highlightBox* updates
            
            # if highlightBox is starting this frame...
            if highlightBox.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                highlightBox.frameNStart = frameN  # exact frame index
                highlightBox.tStart = t  # local t and not account for scr refresh
                highlightBox.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(highlightBox, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'highlightBox.started')
                # update status
                highlightBox.status = STARTED
                highlightBox.setAutoDraw(True)
            
            # if highlightBox is active this frame...
            if highlightBox.status == STARTED:
                # update params
                pass
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=practice_rating,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                practice_rating.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if practice_rating.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in practice_rating.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "practice_rating" ---
        for thisComponent in practice_rating.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for practice_rating
        practice_rating.tStop = globalClock.getTime(format='float')
        practice_rating.tStopRefresh = tThisFlipGlobal
        thisExp.addData('practice_rating.stopped', practice_rating.tStop)
        # check responses
        if practiceRating.keys in ['', [], None]:  # No response was made
            practiceRating.keys = None
        trials.addData('practiceRating.keys',practiceRating.keys)
        if practiceRating.keys != None:  # we had a response
            trials.addData('practiceRating.rt', practiceRating.rt)
            trials.addData('practiceRating.duration', practiceRating.duration)
        # Run 'End Routine' code from code_2
        highlightBox.autoDraw = False
        
        
        # the Routine "practice_rating" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        # mark thisTrial as finished
        if hasattr(thisTrial, 'status'):
            thisTrial.status = FINISHED
        # if awaiting a pause, pause now
        if trials.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            trials.status = STARTED
        thisExp.nextEntry()
        
    # completed 1.0 repeats of 'trials'
    trials.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    # get names of stimulus parameters
    if trials.trialList in ([], [None], None):
        params = []
    else:
        params = trials.trialList[0].keys()
    # save data for this loop
    trials.saveAsExcel(filename + '.xlsx', sheetName='trials',
        stimOut=params,
        dataOut=['n','all_mean','all_std', 'all_raw'])
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
