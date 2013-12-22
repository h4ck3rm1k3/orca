import orca.settings_manager as sm
import pprint 
import  orca.settings as settings

from orca.script import Script
class App():
    @property
    def name(self):
        return "bla"
app=App()

s = Script(app=app)
# settings
# settings.activeProfile
# settings.allTextAttributes
# settings.ariaLandmarks
# settings.asyncMode
# settings.brailleAlignmentMargin
# settings.brailleAlignmentStyle
# settings.brailleBindingsMap
# settings.brailleContractionTable
# settings.brailleEOLIndicator
# settings.brailleFlashTime
# settings.brailleForceRoles
# settings.brailleLinkIndicator
# settings.brailleMaximumJump
# settings.brailleRolenameStyle
# settings.brailleSelectorIndicator
# settings.brailleTableCellDelimiter
# settings.brailleVerbosityLevel
# settings.cacheAccessibles
# settings.cacheDescriptions
# settings.cacheValues
# settings.capitalizationStyle
# settings.chatAnnounceBuddyTyping
# settings.chatMessageVerbosity
# settings.chatRoomHistories
# settings.chatSpeakRoomName
# settings.debugEventQueue
# settings.defaultModifierMask
# settings.disableBrailleEOL
# settings.doubleClickTimeout
# settings.enableActionKeys
# settings.enableBraille
# settings.enableBrailleContext
# settings.enableBrailleGrouping
# settings.enableBrailleMonitor
# settings.enableContractedBraille
# settings.enableCustomScripts
# settings.enableDiacriticalKeys
# settings.enableEchoByCharacter
# settings.enableEchoBySentence
# settings.enableEchoByWord
# settings.enableFlashMessages
# settings.enableFunctionKeys
# settings.enableKeyEcho
# settings.enableMnemonicSpeaking
# settings.enableModifierKeys
# settings.enableMouseReview
# settings.enableNavigationKeys
# settings.enablePauseBreaks
# settings.enablePositionSpeaking
# settings.enablePrintableKeys
# settings.enableProgressBarUpdates
# settings.enableSpeech
# settings.enableSpeechCallbacks
# settings.enableSpeechIndentation
# settings.enableTutorialMessages
# settings.enabledBrailledTextAttributes
# settings.enabledSpokenTextAttributes
# settings.excludeKeys
# settings.flashIsPersistent
# settings.flashVerbosityLevel
# settings.gilSleepTime
# settings.ignoredEventsList
# settings.inferLiveRegions
# settings.keyBindingsMap
# settings.keyboardLayout
# settings.largeObjectTextLength
# settings.messageVerbosityLevel
# settings.mouseDwellDelay
# settings.mouseDwellMaxDrift
# settings.onlySpeakDisplayedText
# settings.orcaModifierKeys
# settings.overrideDisabledMainWindow
# settings.overrideKeyBindings
# settings.overridePronunciations
# settings.presentDateFormat
# settings.presentLockingKeys
# settings.presentReadOnlyText
# settings.presentRequiredState
# settings.presentTimeFormat
# settings.presentToolTips
# settings.profile
# settings.progressBarUpdateInterval
# settings.progressBarVerbosity
# settings.pyatspi
# settings.readTableCellRow
# settings.repeatCharacterLimit
# settings.sayAllStyle
# settings.silenceSpeech
# settings.skipBlankCells
# settings.sounds
# settings.speakBlankLines
# settings.speakCellCoordinates
# settings.speakCellHeaders
# settings.speakCellSpan
# settings.speakMultiCaseStringsAsWords
# settings.speechFactoryModules
# settings.speechPitchDelta
# settings.speechRateDelta
# settings.speechServerFactory
# settings.speechServerInfo
# settings.speechVerbosityLevel
# settings.startingProfile
# settings.synchronousToolkits
# settings.textAttributesBrailleIndicator
# settings.timeoutCallback
# settings.timeoutTime
# settings.tty
# settings.useBlockPreventor
# settings.useExperimentalSpeechProsody
# settings.useGILIdleHandler
# settings.userCustomizableSettings
# settings.verbalizePunctuationStyle
# settings.voices
# settings.voicesKeys
# settings.wrappedStructuralNavigation


o = sm.SettingsManager()

#for x in dir(settings):
#    print("settings.%s" % x)
    #print(getattr(o,x).__help__)

pprint.pprint(o.getSetting('voices'))

pprint.pprint(o.activate())
pprint.pprint(o.availableProfiles())
pprint.pprint(o.backendModule)
pprint.pprint(o.backendName)
pprint.pprint(o.customizedSettings) # dict
pprint.pprint(o.defaultGeneral) # dict
pprint.pprint(o.defaultGeneralValues)
pprint.pprint(o.defaultKeybindings)
pprint.pprint(o.defaultPronunciations)
pprint.pprint(o.general)
pprint.pprint(o.getGeneralSettings())
pprint.pprint(o.getKeybindings())
pprint.pprint(o.getPreferences())
pprint.pprint(o.getPrefsDir())
pprint.pprint(o.getProfile())
pprint.pprint(o.getPronunciations())
pprint.pprint(o.getSetting(settingName="voices"))
pprint.pprint(o.getVoiceLocale())
pprint.pprint(o.isAccessibilityEnabled())
pprint.pprint(o.isFirstStart())
pprint.pprint(o.isScreenReaderServiceEnabled())
pprint.pprint(o.keybindings) # dict



pprint.pprint(o.loadAppSettings(script=s))

pprint.pprint(o.overrideKeyBindings(script=s,scriptKeyBindings=None))
pprint.pprint(o.profile) # dict
pprint.pprint(o.profileGeneral) # dict
pprint.pprint(o.profileKeybindings) # dict
pprint.pprint(o.profilePronunciations) # dict
pprint.pprint(o.pronunciations) # dict
pprint.pprint(o.saveSettings(
    general={},
    pronunciations={}, 
    keybindings={}
))
pprint.pprint(o.setAccessibility(enable=True))
pprint.pprint(o.setFirstStart())
pprint.pprint(o.setProfile())
pprint.pprint(o.setSetting(
    settingName="blg",
    settingValue="val"
))
pprint.pprint(o.setStartingProfile())
pprint.pprint(o.settingsPackages) # list
