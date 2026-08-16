import sys
import os
from panda3d.core import loadPrcFileData, Vec3
import random


def resource_path(relative_path):
    """Return the correct path for normal Python runs and PyInstaller one-file builds."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

from direct.interval.IntervalGlobal import LerpFunc, Sequence, Func, Wait


# 1. FENSTER-EINSTELLUNGEN (Für Mac-Stabilität & schwarzen Hintergrund)
loadPrcFileData("", "load-display pandagl")
loadPrcFileData("", "gl-version 3 2")

# Fenster-Einstellungen (Größe fest, kein Fullscreen beim Start)
loadPrcFileData("", "window-title The Lamp (by Varto)")
loadPrcFileData("", "win-size 1080 720")
loadPrcFileData("", "fullscreen #f")
loadPrcFileData("", f"icon-filename {resource_path('photos/Bildschirmfoto 2026-06-14 um 23.49.10.ico')}") 

# Grafik & Performance
loadPrcFileData("", "win-background-color 0 0 0")

loadPrcFileData("", "framebuffer-multisample 1")
loadPrcFileData("", "multisamples 4") 
loadPrcFileData("", "gamma 0.5 #t")
loadPrcFileData("", "aspect-ratio 1.5")
loadPrcFileData("", "keep-alive-truncation #t")
loadPrcFileData("", "win-size 1080 720")
loadPrcFileData("", "framebuffer-min-width 320")
loadPrcFileData("", "framebuffer-min-height 240")
# WICHTIG: Das hier verhindert das "Verschmieren" der Pixel beim Skalieren
loadPrcFileData("", "texture-minfilter nearest")
loadPrcFileData("", "texture-magfilter nearest")


# Wichtig: Keine Kantenglättung (Multisamples 0)
loadPrcFileData("", "framebuffer-multisample 0")
loadPrcFileData("", "multisamples 0")

# Das hier ist der "Master-Schalter" für harte Pixel:
loadPrcFileData("", "texture-minfilter nearest")
loadPrcFileData("", "texture-magfilter nearest")


# In deiner __init__ oder in der Kapitel_1-Funktion:
# Aktiviere den PBR-Pipeline für das Modell

           # Zwingt Panda3D zu einem moderneren OpenGL-Standard


# Force Panda3D to use the advanced Assimp plugin for OBJ files
loadPrcFileData("", "load-file-type p3assimp")

from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from direct.interval.IntervalGlobal import LerpFunc, Sequence, Func
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CardMaker, MovieTexture

class HorrorGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0)

        # Texture-Suchpfade SOFORT konfigurieren (BEVOR irgendwelche Modelle geladen werden!)
        from panda3d.core import get_model_path
        texture_path = resource_path('Models/textures')
        get_model_path().prepend_path(texture_path)  # prepend = höchste Priorität
        print(f"✓ Model-Suchpfade konfiguriert:")
        print(f"  - Texture-Pfad: {texture_path}")

        
    

        
       
        from panda3d.core import CollisionSphere, CollisionNode

        # Kamera eine Kollisions-Kugel geben
        cnode = CollisionNode('camera')
        cnode.addSolid(CollisionSphere(0, 0, 0, 0.5)) # 0.5 ist der Radius um die Kamera
        cnode.setIntoCollideMask(0) # Die Kamera soll selbst nichts blockieren
        cnode.setFromCollideMask(1) # Die Kamera soll aber an Maske 1 abprallen
        self.camera_col = self.camera.attachNewNode(cnode)
        
        # Mauszeiger aktivieren
        self.disableMouse()  
        from panda3d.core import WindowProperties
        props = WindowProperties()
        props.setCursorHidden(False)
        self.win.requestProperties(props)
        
        # Schriften laden
        zapfino_path = "/System/Library/Fonts/Supplemental/Zapfino.ttf"
        if os.path.exists(zapfino_path):
            self.game_font = loader.loadFont(zapfino_path)
        else:
            self.game_font = loader.loadFont("cmss12")
        if not self.game_font:
            self.game_font = TextNode.getDefaultFont()


        horror_font_path = "/System/Library/Fonts/Supplemental/AmericanTypewriter.ttc"
        avenir_condensed_path2 = "/System/Library/Fonts/Supplemental/Avenir Next Condensed.ttf"
        if os.path.exists(horror_font_path):
            self.game_font3 = loader.loadFont(horror_font_path)
            print("Horror-Font geladen!")
        elif os.path.exists(avenir_condensed_path2):
            self.game_font3 = loader.loadFont(avenir_condensed_path2)
            print("Fallback-Font geladen!")
        else:
            self.game_font3 = loader.loadFont("cmss12")
        if not self.game_font3:
            self.game_font3 = TextNode.getDefaultFont()
            
        self.game_font1 = self.game_font
        avenir_condensed_path = "/System/Library/Fonts/Avenir Next Condensed.ttc"
        arial_narrow_path = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"
        if os.path.exists(avenir_condensed_path):
            self.game_font1 = loader.loadFont(avenir_condensed_path)
        elif os.path.exists(arial_narrow_path):
            self.game_font1 = loader.loadFont(arial_narrow_path)
        self.Mouse1_ist_erstmal_linked_zur_einer_func = True
        self.settings_gerade = False

        # Tastatur/Maus-Abfrage einrichten
        self.keys = {"mouse1": False, "w": False, "d": False, "s": False, "a": False, "r": False, "shift": False}
       
        
        self.accept("mouse1-up", self.set_key, ["mouse1", False])
        self.accept("mouse1", lambda: [self.set_key("mouse1", True), self.on_mouse_click()])
        self.accept("w", self.set_key, ["w", True])
        self.accept("w-up", self.set_key, ["w", False])
        self.accept("d", self.set_key, ["d", True])
        self.accept("d-up", self.set_key, ["d", False])
        self.accept("s", self.set_key, ["s", True])
        self.accept("s-up", self.set_key, ["s", False])
        self.accept("a", self.set_key, ["a", True])
        self.accept("a-up", self.set_key, ["a", False])
        self.accept("r", self.set_key, ["r", True]) 
        self.accept("shift", self.set_key, ["shift", True])
        self.accept("shift-up", self.set_key, ["shift", False])
        self.accept("escape", self.Pause) 
         # Escape-Taste zum Beenden des Spiels

        # Texte erstellen
        self.maus_anzeige = OnscreenText(text="Warte auf Maus...", pos=(0, -0.9), scale=0.05, fg=(1, 1, 1, 0), align=TextNode.ACenter, mayChange=True)
        self.beginnen_text = OnscreenText(text="", pos=(0, -0.73), scale=0.05, fg=(1, 1, 1, 0), align=TextNode.ACenter, mayChange=True)
        self.Title = OnscreenText(text="The Lamp", pos=(0, 0), scale=0.3, fg=(1, 0, 0, 0), align=TextNode.ACenter, font=self.game_font, mayChange=True)
        self.timer_text = OnscreenText(text="Time passed: 0", pos=(0, 0.8), scale=0.05, fg=(1, 1, 1, 0), align=TextNode.ACenter, mayChange=True)
        self.narrative_text = OnscreenText(text="", pos=(0, 0), scale=0.05, fg=(1, 1, 1, 0), align=TextNode.ACenter, mayChange=True)
        self.Autor = OnscreenText(text="", pos=(0,0), scale=0.2, fg=(1,1,1,1), align=TextNode.ACenter, mayChange=True)
        self.tipp_text = OnscreenText(text="", pos=(0, -0.5), scale=0.07, fg=(1, 1, 1, 1), mayChange=True)
        self.tipp_text.setFont(self.game_font3)
        self.Hpr_text = OnscreenText(text="", pos=(0, 0.60), scale=0.05, fg=(1, 1, 1, 1), align=TextNode.ACenter, mayChange=True)
        self.Cordinates_for_camera = OnscreenText(text="", pos=(0, 0.73), scale=0.061, fg=(1, 1, 1, 1), align=TextNode.ACenter, mayChange=True)
        self.zeige_interaktions_text = OnscreenText(text="", pos=(0, -0.24), scale= 0.056, fg=(1, 1, 1, 1), align=TextNode.ACenter, mayChange=True)
        self.Autor.setFont(self.game_font1)
        self.video3 = MovieTexture("menu_video")
        self.video_path_menu = resource_path('videos/0607-Kopie-Kopie(1).mp4')
        if self.video3.read(self.video_path_menu):
          self.video3.setLoopCount(0)
        
        # 1. Sounds vorab laden
        self.hover_sound = loader.loadSfx(resource_path('sounds/justsomesounds-click-sound-432501.mp3'))
        self.Text_Blip_sound = loader.loadSfx(resource_path('sounds/468925__malakme__high-text-blip.ogg'))
        self.Ringtone = loader.loadSfx(resource_path('sounds/sdanezis-cell-phone-ringtone-01-sfx-317313.mp3'))
        self.FlashBang = loader.loadSfx(resource_path('sounds/Flashbang.mp3'))
        self.Musik_Piano = loader.loadSfx(resource_path('music/gregorquendel-dreamlike-piano-and-strings-soundscape-291600 Kopie.mp3'))

        #self.Ticking_sound = loader.loadSfx(resource_path('sounds/Tick_Tack.mp3'))
        
        # 2. Bilder vorab laden und verstecken
        self.video_path8 = resource_path('photos/arrow-return-or-reply-white-color-icon-vector.jpg')
        self.mein_bild2 = OnscreenImage(image=self.video_path8, pos=(-0.9, 0, 0.9), scale=0.1)
        self.mein_bild2.setTransparency(True)
        self.mein_bild2.hide() 
        self.Audio_vom_Video = loader.loadSfx(resource_path('sounds/freesound_community-medium-text-blip-14855.mp3')) # Standardmäßig unsichtbar
        self.Lampe_click = loader.loadSfx(resource_path('sounds/Boom.mp3'))
        self.Walking_sound = loader.loadSfx(resource_path('sounds/Walking.mp3'))
        self.Glitch_Sfx = loader.loadSfx(resource_path('sounds/Glitch.mp3'))
        self.Boom = loader.loadSfx(resource_path('sounds/SlowBoom.mp3'))
        self.Dream5 = loader.loadSfx(resource_path('sounds/Dream.mp3'))
        self.Hospitel_Sound = loader.loadSfx(resource_path('sounds/freesound_community-steadyheartratemonitorloop1min-6274.mp3'))
        self.Atmen_Sound = loader.loadSfx(resource_path('sounds/freesound_community-heavy-breathing-14431.mp3'))
        self.Riser = loader.loadSfx(resource_path('sounds/dragon-studio-cinematic-riser-03-414575'))
        self.Door_slam = loader.loadSfx(resource_path('sounds/freesound_community-door-slam-angrily-86963.mp3'))
        self.Musik_Piano = loader.loadSfx(resource_path('music/gregorquendel-dreamlike-piano-and-strings-soundscape-291600 Kopie.mp3'))
        # 3. Zusätzliche Videos vorab laden
        self.video4 = MovieTexture("menu_videoo")
        self.video_path7 = resource_path('videos/0607-Kopie-Kopie(2).mp4')
        if self.video4.read(self.video_path7):
            self.video4.setLoopCount(0)
            self.video4.stop()         # <--- NEU: Verhindert, dass das Video im Hintergrund unbemerkt läuft
            self.video4.setTime(0.0)

        cm = CardMaker("text_bg")
        cm.setFrame(-0.27, 0.27, -0.08, 0.08) # Die Größe anpassen, je nachdem wie lang der Text ist
        self.text_bg = render2d.attachNewNode(cm.generate())
        self.text_bg.setColor((0, 0, 0, 0.6)) # Schwarz mit 80% Deckkraft (leicht transparent)
        self.text_bg.setPos(0, 0, -0.5)       # Gleiche Position wie dein Text
        self.text_bg.hide()                # Erstmal verstecken
        
        # Schutzschalter für Animationen und Sounds
        self.animation_gestartet = False
        self.ausblenden_gestartet = False
        self.meine_musikspielt = False
        self.hover_sound_gespielt = False  
        self.sound_check = False
        self.Capcut_Scene = False
        self.sound_check9 = False
        self.Check_for_cordinates = False
        self.Intro_Animation_gestartet = False
        self.ambient_sound_gestartet = False
        self.sound_check10 = False
        self.hover_sound_gespielt = False
        self.Mouse1_ist_erstmal_linked_zur_einer_func = True
        self.Taste_an = True
        self.game_startet = False
        self.Knopf_bereit_damit_Ui_clickbar_ist_für_pause_menu = False
        self.ready_for_game = True
        self.erlaubt_für_Ui_settings = True
        self.Audio_check = False
        self.Settings_knopf = False
        self.zurück_gehen_ist_erlaubt = False
        self.Kapitel_2_beginn = False
        self.jumpscare_passiert = False
        self.Kapitel_1_Auto_kommt_gestartet = False
        self.sound_check13 = False
        self.Glitch_Szene = False
        self.sound_check14 = False
        self.sound_check15 = False
        self.sound_check16 = False
        self.Gravitation = True
        self.RollCamera = False

        self.a = 1 
        self.b = 0 
        self.d = 0
        self.c = 0
        self.e = 0
        self.f = 1 
        self.g = 0
        self.z = 1
        self.sound_check12 = False
        # Check wenn der 3d Part startet
        
        self.animation_gestartet1 = False
        
        # Tasks starten
        self.taskMgr.add(self.update_mouse_task, "UpdateMouseTask")
        self.taskMgr.add(self.time_manager, "TimeManagerTask")
        self.taskMgr.add(self.Vector3_updater_to_player, "MovementTask")
        self.taskMgr.add(self.updater_fpr_sounds, "SoundUpdateTask")
        self.taskMgr.add(self.update_H_of_camera, "CameraUpdateTask")
        self.taskMgr.add(self.check_interaktion, "BitteWork")
        

      
       
        
    def time_manager(self, task):
        sekunden = int(task.time)
        #self.timer_text.setText(f"Time passed: {sekunden}")
        
        if sekunden > 1 and not self.animation_gestartet1:
            self.animation_gestartet1 = True 
            
            
            

            #self.Autor.setText("A Psychological Horror Game by Varto")
            #self.Autor.setScale(0.1)
            #self.Autor.setFont(self.game_font)
            #if not self.sound_check:
                #self.sound_check = True
                #self.Sound_Lampe = loader.loadSfx(resource_path('sounds/dragon-studio-light-switch-382712.mp3'))
                #self.Sound_Lampe.play()

        #if sekunden == 3:
            #self.Autor.setFg((1,1,1,1))

           

        if sekunden > 2 and not self.animation_gestartet and not self.Intro_Animation_gestartet:
            self.animation_gestartet = True 
            self.Intro_Animation_gestartet = True
            self.beginnen_text.setText("Left click to begin!")
            self.beginnen_text.setFg((1, 1, 1, 1))
            self.beginnen_text.setFont(self.game_font1)
            self.video_path6 = resource_path('photos/images.jpeg')
            #self.mein_bild = OnscreenImage(image=self.video_path6, pos=(1, 0.90, 0.90), scale=0.05)
            #self.mein_bild.setTransparency(True)
          
        


            self.video_path = resource_path('videos/0607-Kopie.mp4')
            
            
                      # 2. MovieTexture korrekt erstellen und laden
            self.video2 = MovieTexture("mein_video_loop")
            if self.video2.read(self.video_path):
              self.video2.setLoopCount(0) 
                
                      # 3. Fullscreen-Fläche für das Video erstellen und an render2d hängen
              cm = CardMaker("video_plane")
              cm.setFrame(-1.5, 1.8, -1.2, 1.7) 
              self.video_flaeche2 = render2d.attachNewNode(cm.generate())
              self.video_flaeche2.setPos(0.5, 1, 0.16)
                
              # 4. Video auf die Fläche legen und abspielen
              self.video_flaeche2.setTexture(self.video2)
              self.video2.play()
              self.Humming_sound = loader.loadSfx(resource_path('sounds/dewyproductions2022-real-vhs-169982.mp3'))
              self.Humming_sound.setLoop(True)
              self.Humming_sound.play()
              

        



            
            
              
            
       # if self.Check_for_cordinates:

             # Mensch_pos = self.camera.getPos()
              #self.Cordinates_for_camera.setText(f"Camera Position: ({Mensch_pos.x:.2f}, {Mensch_pos.y:.2f}, {Mensch_pos.z:.2f})")
              
        return task.cont
    


    def starte_fade_in(self):
        from panda3d.core import CardMaker
        cm = CardMaker("black_overlay")
        cm.setFrame(-10, 10, -10, 10)
        self.black_overlay = render2d.attachNewNode(cm.generate())
        self.Lampe_click.play()
        self.black_overlay.setColor(0, 0, 0, 0)  # Startet transparent
        self.black_overlay.setTransparency(True)
        self.black_overlay.setBin("fixed", 30)  # Über allem anderen rendern
        self.black_overlay.setDepthTest(False)
        self.black_overlay.setDepthWrite(False)

        # Store reference to avoid deletion issues during animation
        overlay_ref = self.black_overlay
        
        # Fade-In Animation starten
        def update_alpha(alpha):
            if overlay_ref and overlay_ref.getParent():
                overlay_ref.setColor(0, 0, 0, alpha)
        
        fade_in_interval = LerpFunc(
            update_alpha,
            fromData=1,
            toData=0,
            duration=5.0,
            blendType='easeInOut'
        )
        fade_in_interval.start()
       
    def starte_schreib_animation(self, voller_text):
        self.tipp_text.show()
        self.text_bg.show()
        self.tipp_text.setFont(self.game_font3)
        self.voller_text = voller_text
        self.aktuelle_laenge = 0 
        self.taskMgr.add(self.schreib_task, "SchreibAnimation")


    def schreib_task(self, task):
        if self.aktuelle_laenge < len(self.voller_text):  
            self.aktuelle_laenge += 1
            self.tipp_text.setText(self.voller_text[:self.aktuelle_laenge])
            
            # Dynamische Breite berechnen (passt sich an wachsenden Text an!)
            breite = len(self.voller_text[:self.aktuelle_laenge]) * 0.0427
            self.text_bg.setScale(breite, 1, 1)
            
            if self.Audio_check == False and self.b ==1 :
              self.Audio_check = True
              self.Audio_vom_Video.play()
            if self.Audio_check and self.c == 1:
              self.Text_Blip_sound.play()
              
              self.Audio_check = False

            # Die Geschwindigkeit: 0.1 Sekunden pro Buchstabe
            # Ich baue ein Notfallsysten ein, weil ich öfters das Problem hatte, dass die Texte gehidet sind.
            self.tipp_text.show()
            self.text_bg.show()
            task.delayTime = 0.1
            return task.again
        else:
            if hasattr(self, 'Text_Blip_sound'):
                self.Text_Blip_sound.stop()
            if hasattr(self, 'Audio_vom_Video'):
                self.Audio_vom_Video.stop()
           
             
            hide_sequence = Sequence(Wait(3), Func(self.tipp_text.hide), Func(self.text_bg.hide))
            hide_sequence.start()
            self.Audio_check = False
            return task.done


    def on_mouse_click(self):
       
        
        self.Mouse1_ist_erstmal_linked_zur_einer_func = True
        
        
        if self.mouseWatcherNode.hasMouse():
            pos = self.mouseWatcherNode.getMouse()
            x = pos.getX()
            y = pos.getY()
            
            
            if 0.58 < x < 0.75 and 0.67 < y < 0.75 and   self.game_startet == False and self.keys["mouse1"]:
                
                self.settings_gerade = True
                self.Settings_knopf = True
                self.zurück_gehen_ist_erlaubt = True
                self.beginnen_text.setText("")
                
               
                self.mein_bild2.show()
                
                cm = CardMaker("video_plane")
                cm.setFrame(-1.8, 1.8, -1.8, 1) 
                self.video_flaeche3 = render2d.attachNewNode(cm.generate())
                self.video_flaeche3.setTexture(self.video3)
                self.video3.play()
                self.video_flaeche3.setPos(0.71, 0, 0.76)
                
                if hasattr(self, 'video_flaeche2'):
                    self.video_flaeche2.removeNode()
                self.ready_for_game = False
                self.hover_sound.play()
                self.beginnen_text.setFg((1, 1, 1, 1))
    
                if not hasattr(self, 'Humming_sound'):
                    self.Humming_sound.play()
            
            
            if -0.12 < x < 0.16 and -0.46 < y < -0.35 and self.Settings_knopf == True :
                
                self.erlaubt_für_Ui_settings = True
                self.zurück_gehen_ist_erlaubt = True
                self.Settings_knopf = False
                self.hover_sound.play()
                self.beginnen_text.setText("Left click to beginn!")
                
                if hasattr(self, 'video_flaeche3'):
                    self.video_flaeche3.removeNode()

                
                cm = CardMaker("video_plane")
                cm.setFrame(-1.2, 1, -1.8, 1) 
                self.video_flaeche4 = render2d.attachNewNode(cm.generate())
                self.video_flaeche4.setPos(0.2, 1, 1.1)
                
                
                self.mein_bild2.show()
                self.video_flaeche4.setTexture(self.video4)
                
                self.video4.play()
                self.beginnen_text.setText("")
                
    
           
            if -0.16 < x < 0.19 and -0.12 < y < 0.02 and self.Settings_knopf and not self.game_startet:
                
                if hasattr(self, 'video_flaeche3'):
                    self.video_flaeche3.removeNode()

                    self.hover_sound.play()
                    cm = CardMaker("video_plane")
                    cm.setFrame(-1.5, 1.8, -1.2, 1.7) 
                    self.video_flaeche2 = render2d.attachNewNode(cm.generate())
                    self.video_flaeche2.setPos(0.5, 1, 0.16)

                    # Textur neu verbinden und starten
                    self.video2.setTime(0.0)
                    self.video_flaeche2.setTexture(self.video2)
                    self.video2.play()
                    self.settings_gerade = True
                    self.Settings_knopf = False
                    self.beginnen_text.setText("Left click to beginn!")
                    
            
            if -0.05 < x < 0.09 and 0.20 < y < 0.33 and self.Settings_knopf and not self.game_startet:
              
                self.hover_sound.play()
                sys.exit()
                
            
            if -0.54 < x < 0.40 and -0.01 < y < 0.09 and self.erlaubt_für_Ui_settings and not self.game_startet:
                
                self.set_master_volume(0.2)
                self.hover_sound.play()
                
            if -0.10 < x < 0.13 and -0.01 < y < 0.09 and self.erlaubt_für_Ui_settings and not self.game_startet:
                
                self.set_master_volume(0.5)
                self.hover_sound.play()
                
            if 0.40 < x < 0.54 and -0.01 < y < 0.09 and self.erlaubt_für_Ui_settings and not self.game_startet:
                
                self.set_master_volume(1.0)
                self.hover_sound.play()
                
            
            if -0.63 < x < -0.56 and 0.87 < y < 0.92 and self.zurück_gehen_ist_erlaubt and not self.game_startet: 
                
                self.zurück_gehen_ist_erlaubt = False
                self.erlaubt_für_Ui_settings = False
                self.Settings_knopf = False
                self.hover_sound.play()
                self.settings_gerade = True

                if hasattr(self, 'video_flaeche4'):
                    self.video_flaeche4.removeNode()
                if hasattr(self, 'video_flaeche3'):
                    self.video_flaeche3.removeNode()
                
                if hasattr(self, 'video_flaeche2'):
                    self.video_flaeche2.removeNode()

                    # Fläche neu bauen
                    cm = CardMaker("video_plane")
                    cm.setFrame(-1.5, 1.8, -1.2, 1.7) 
                    self.video_flaeche2 = render2d.attachNewNode(cm.generate())
                    self.video_flaeche2.setPos(0.5, 1, 0.16)

                    
                    self.video2.setTime(0.0)
                    self.video_flaeche2.setTexture(self.video2)
                    self.video2.play()
                    self.beginnen_text.setText("Left click to beginn")
            # Pausen Menü vom 3d Teil aus aufrufen
            if -0.12 < x < 0.16 and -0.46 < y < -0.35 and self.Settings_knopf == True and self.game_startet:
                
                self.erlaubt_für_Ui_settings = True
                self.zurück_gehen_ist_erlaubt = True
                self.Settings_knopf = False
                self.hover_sound.play()
                
                if hasattr(self, 'video_flaeche3'):
                    self.video_flaeche3.removeNode()

                
                cm = CardMaker("video_plane")
                cm.setFrame(-1.2, 1, -1.8, 1) 
                self.video_flaeche4 = render2d.attachNewNode(cm.generate())
                self.video_flaeche4.setPos(0.2, 1, 1.1)
                
                
                self.mein_bild2.show()
                self.video_flaeche4.setTexture(self.video4)
                
                self.video4.play()
                
    
           
            if -0.16 < x < 0.19 and -0.12 < y < 0.02 and self.Settings_knopf and self.game_startet: 
                
                if hasattr(self, 'video_flaeche3'):
                    self.video_flaeche3.removeNode()
                    self.hover_sound.play()
                if hasattr(self, 'video_flaeche2'):
                    self.video_flaeche2.removeNode()
                   
                    self.settings_gerade = True
                    self.Settings_knopf = False
                    self.Pause()
                    
            
            if -0.05 < x < 0.09 and 0.20 < y < 0.33 and self.Settings_knopf and self.game_startet:
              
                self.hover_sound.play()
                sys.exit()

                
            
            if -0.54 < x < 0.40 and -0.01 < y < 0.09 and self.erlaubt_für_Ui_settings and self.game_startet:
                
                self.set_master_volume(0.2)
                self.hover_sound.play()
                
            if -0.10 < x < 0.13 and -0.01 < y < 0.09 and self.erlaubt_für_Ui_settings and self.game_startet:
                
                self.set_master_volume(0.5)
                self.hover_sound.play()
                
            if 0.40 < x < 0.54 and -0.01 < y < 0.09 and self.erlaubt_für_Ui_settings and self.game_startet:
                
                self.set_master_volume(1.0)
                self.hover_sound.play()
                
            
            if -0.63 < x < -0.56 and 0.87 < y < 0.92 and self.zurück_gehen_ist_erlaubt and self.game_startet:
                
                self.zurück_gehen_ist_erlaubt = False
                self.erlaubt_für_Ui_settings = False
                self.Settings_knopf = False
                self.hover_sound.play()
                self.settings_gerade = True
                self.mein_bild2.hide()
                self.Pause()

                if hasattr(self, 'video_flaeche4'):
                    self.video_flaeche4.removeNode()
                if hasattr(self, 'video_flaeche3'):
                    self.video_flaeche3.removeNode()
                
                
                 
       
    def starte_auto_event2(self, task):
        model_path = resource_path('Models/old_rusty_car_2.glb')
        self.Auto_Modell = loader.loadModel(model_path)
        self.Auto_Modell.reparentTo(render)
        self.Auto_Modell.setPos(60, -90, 0)
        self.Auto_Modell.setHpr(0, -270, 0)
        self.Auto_Modell.setScale(0.0277)
        self.z = 0
        def set_fov_and_look(fov_wert):
              self.camLens.setFov(fov_wert)  # self.camLens, nicht base.camLens!
              self.camera.lookAt(self.Auto_Modell)  # Kontinuierlich auf Auto schauen!

        # Speichere Intervall in self damit es nicht gelöscht wird:
        self.Auto_angucken_Intervall = LerpFunc(
              set_fov_and_look,
              fromData=80,
              toData=35,
              duration=3.5,
          )
        self.Auto_angucken_Intervall.start()
        
        
        def Normal_gucken(fov_wert):
            self.camLens.setFov(fov_wert) 

        Normal_gucken_Intervall = LerpFunc(
                Normal_gucken,
                fromData=35,
                toData=80,
                duration=1.2,
            )
        Sequence(
            Wait(5),  # Warte, bis die erste Intervall fertig ist
            Func(Normal_gucken_Intervall.start)  # Starte die zweite Intervall
        ).start()
              

        LerpFunc(lambda a: self.Auto_Modell.setPos(60, a, 0), fromData=-90, toData=200, duration=7).start()
        
        Car_passing_by = loader.loadSfx(resource_path('sounds/soundreality-car-passing-city-364146.mp3'))
       
        Car_passing_by.play()
        
        Car_passing_by.setVolume(0.5)


        return task.done

    def Dialouge_vom_protagonisten(self, task):
       
        dialogue_sequence = Sequence(
            Func(self.starte_schreib_animation, " YOU: what was that... why was the car driving backwards?"),
            Wait(10.5),
            Func(self.starte_schreib_animation, " YOU: lets just go home and finally end it...")
        )
        dialogue_sequence.start()
       
        
       
                          
        return task.done

        
                   
    def Show_The_Car(self):
       
       sequence8 = Sequence(
         Wait(0.1),
         Func(self.Auto_Modell.copyTo(render)),
         Wait(0.1),
         Func(self.Auto_Modell.setPos, self.camera.getX(), self.camera.getY() - 10, 1),
         Wait(0.45),
         Func(self.Auto_Modell.removeNode)
       )
        
         
       sequence8.start()
       
      
    def starte_auto_event(self):
          model_path = resource_path('Models/old_rusty_car_2.glb')
          self.Auto_Modell1 = loader.loadModel(model_path)
          self.Auto_Modell1.reparentTo(render)
          self.Auto_Modell1.setPos(-56.5, -80, 0)
          self.Auto_Modell1.setHpr(180, -270, 0)
          self.Auto_Modell1.setScale(0.0277)
          self.Taste_an = False
          
          # FOV verändern + Kamera kontinuierlich auf Auto richten
         
         
         
        
         
          LerpFunc(lambda a: self.Auto_Modell1.setPos(-56.5, a, 0), fromData=-70, toData=5, duration=0.5).start()
          #LerpFunc(lambda a: self.Auto_Modell.setH(a), fromData=180, toData=200, duration=1).start()
          #LerpFunc(lambda a: self.Auto_Modell.setX(a), fromData=-55.5, toData=-56, duration=1).start()
        
          car_crash = loader.loadSfx(resource_path('sounds/pwlpl-car_crash-377291.mp3'))
          car_crash.play()

    def Vector3_updater_to_player(self, task):
            # Wir bewegen die Kamera relativ zu sich selbst
        if self.keys["w"] and self.Taste_an:
            self.camera.setPos(self.camera, Vec3(0, 0.05, 0))
        if self.keys["w"] and self.keys["shift"] and self.Taste_an and self.z == 1:
            self.camera.setPos(self.camera, Vec3(0, 0.07, 0))
            if self.e == 0:
              if hasattr(self, 'Schritte_sound'):
                self.Schritte_sound.setPlayRate(1.95)
            if self.e == 1:
               if hasattr(self, 'Walking_sound'):
                self.Walking_sound.setPlayRate(1.95)
        else:
            if hasattr(self, 'Schritte_sound'):
              self.Schritte_sound.setPlayRate(1.0)
            if hasattr(self, 'Walking_sound'):
              self.Walking_sound.setPlayRate(1.0)
            # 💨 Leichte Screen-Vibration beim Sprinten
            #self.camera.setP(self.camera.getP() + (0.05 if int(task.time * 100) % 2 == 0 else -0.1))
            
        
            
        if self.keys["s"] and self.Taste_an:
            self.camera.setPos(self.camera, Vec3(0, -0.05, 0))
        if self.keys["a"] and self.Taste_an:
            self.camera.setPos(self.camera, Vec3(-0.05, 0, 0))
        if self.keys["d"] and self.Taste_an:
            self.camera.setPos(self.camera, Vec3(0.05, 0, 0))
        if self.keys["r"]:
            self.camera.setPos(self.camera, Vec3(0, 0, 0.1))
        if self.camera.getZ() > 1 or self.camera.getZ() < 1:
           self.camera.setZ(1)
        
        # 🔒 GRENZE - Wenn X zu weit, zurückdrücken
        if self.b == 1 and self.camera.getX() > 55:
            if self.keys["shift"] and self.keys["w"] :
                self.camera.setPos(self.camera, Vec3(0, -0.0767, 0))
                

            if self.keys["w"] and not self.keys["shift"]:
              self.camera.setPos(self.camera, Vec3(0, -0.05, 0)) 
            if self.keys["a"]:
                self.camera.setPos(self.camera, Vec3(0.05, 0, 0))
            if self.keys["d"]:
                self.camera.setPos(self.camera, Vec3(-0.05, 0, 0))
            
            # Ich mach jetzt ein sogenanntes "Ruckeln" , damit es sich so anfühlt als wäre man in einer Simulation, bei der man die Verbindung verliert
           

        else:
            if hasattr(self, 'Glitch_Sound'):
              self.Glitch_Sound.stop()
              self.sound_check10 = False

        if self.b == 1 and self.camera.getY() > -3.76 and self.Kapitel_2_beginn == False and self.d == 0:
            if self.keys["shift"] and self.keys["w"] :
                self.camera.setPos(self.camera, Vec3(0, -0.12, 0))
            if self.keys["a"]:
                self.camera.setPos(self.camera, Vec3(0.05, 0, 0))
            if self.keys["d"]:
                self.camera.setPos(self.camera, Vec3(-0.05, 0, 0))
            if self.keys["w"] and not self.keys["shift"]:
              self.camera.setPos(self.camera, Vec3(0, -0.05, 0))

        if self.b == 1 and self.camera.getY() < -15.23 and self.Kapitel_2_beginn == False and self.d == 0:
            if self.keys["shift"] and self.keys["w"] :
                self.camera.setPos(self.camera, Vec3(0, -0.12, 0))
            if self.keys["a"]:
                self.camera.setPos(self.camera, Vec3(0.05, 0, 0))
            if self.keys["d"]:
                self.camera.setPos(self.camera, Vec3(-0.05, 0, 0))
            if self.keys["w"] and not self.keys["shift"]:
              self.camera.setPos(self.camera, Vec3(0, -0.05, 0)) 
            
            # Ich mach jetzt ein sogenanntes "Ruckeln" , damit es sich so anfühlt als wäre man in einer Simulation, bei der man die Verbindung verliert
            if self.sound_check10 == False and -4.5 < self.camera.getY() < -3.76 and self.Kapitel_2_beginn == False:
              self.sound_check10 = True
              self.Glitch_Sound = loader.loadSfx(resource_path('sounds/dbsound-electrical-issue-affecting-household-appliances-246811.mp3'))
              self.Glitch_Sound.setVolume(1)
              self.Glitch_Sound.play()
        

        else:
            if hasattr(self, 'Glitch_Sound'):
              
              self.Glitch_Sound.stop()
              self.sound_check10 = False

        if 0 < self.camera.getX() < 1 and self.b == 1 and self.jumpscare_passiert == False and self.Kapitel_2_beginn == False and self.d == 0:
            self.jumpscare_passiert = True
            jumpscare_sound = loader.loadSfx(resource_path('sounds/freesound_community-jump-scare-sound-2-82831.mp3'))
            #jumpscare_sound.play()
            self.Horror_music.stop()
            self.Night_ambiente.stop()
            
            def Kopf_dreht_sich(alpha):
                self.camera.setHpr(alpha, 0, 0)
            
            kopf_dreht_sich_interval = LerpFunc(
                Kopf_dreht_sich,
                fromData=90,
                toData=270,
                duration=0.134
            )
            kopf_dreht_sich_interval.start()
            #auto_sequence2 = Sequence(
               
                
                #Wait(0.01),
                #Func(self.starte_auto_event))
            self.taskMgr.doMethodLater(0.15, self.starte_auto_event2, "AutoStartSequence")
            self.taskMgr.doMethodLater(8, self.Dialouge_vom_protagonisten, "Eswirdklappen")


        if self.b == 1:
          H = self.camera.getH()
          P = self.camera.getP()
          R = self.camera.getR()
          #self.Hpr_text.setText(f"H: {H:.2f}, P: {P:.2f}, R: {R:.2f}")


        if -16 < self.camera.getX() < -15 and self.b == 1 and not self.Kapitel_1_Auto_kommt_gestartet and not self.ambient_sound_gestartet and self.Kapitel_2_beginn == False and self.d == 0:
            self.ambient_sound_gestartet = True
            self.Night_ambiente.stop()
            self.Horror_music.stop()
            self.Horror_ambiente_background = loader.loadSfx(resource_path('sounds/tanweraman-dark-rumble-tension-370005.mp3'))
            self.Horror_ambiente_background.setLoop(True)
            self.Horror_ambiente_background.play()

        
        if -57 < self.camera.getX() < -56 and self.b == 1 and not self.Kapitel_1_Auto_kommt_gestartet and self.Kapitel_2_beginn == False and self.d == 0:
            self.Kapitel_1_Auto_kommt_gestartet = True
            self.Taste_an = False  
            
            def set_head_h(h):
                self.camera.setHpr(h, 0, 0)

            auto_sequence = Sequence(
                Wait(2.8),
                LerpFunc(set_head_h, fromData=90, toData=180, duration=0.134),
                Wait(0.01),
                Func(self.starte_auto_event)
            )
            auto_sequence.start()
            self.taskMgr.doMethodLater(3.43, self.Kapitel_2, "KapitelZwei")


        if self.d == 1 and self.b == 1:
            if self.keys["w"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(0, 0.003, 0))
            if self.keys["w"] and self.keys["shift"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(0, 0.003, 0))
                if hasattr(self, 'Schritte_sound'):
                  self.Schritte_sound.setPlayRate(1.95)
            else:
              if hasattr(self, 'Schritte_sound'):
               self.Schritte_sound.setPlayRate(1.0)
            # 💨 Leichte Screen-Vibration beim Sprinten
            #self.camera.setP(self.camera.getP() + (0.05 if int(task.time * 100) % 2 == 0 else -0.1))
            
        
            
              if self.keys["s"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(0, -0.003, 0))
              if self.keys["a"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(-0.003, 0, 0))
              if self.keys["d"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(0.003, 0, 0))
              if self.keys["r"]:
                self.camera.setPos(self.camera, Vec3(0, 0, 0.1))
              if self.camera.getZ() > 1 or self.camera.getZ() < 1:
                self.camera.setZ(1)

        if (self.camera.getY() > 2 or self.camera.getY() < -2) and self.d == 1:
            if self.keys["shift"] and self.keys["w"] :
                self.camera.setPos(self.camera, Vec3(0, -0.20, 0))
            if self.keys["a"]:
                self.camera.setPos(self.camera, Vec3(0.20, 0, 0))
            if self.keys["d"]:
                self.camera.setPos(self.camera, Vec3(-0.20, 0, 0))
            if self.keys["w"] and not self.keys["shift"]:
              self.camera.setPos(self.camera, Vec3(0, -0.20, 0)) 
            if self.keys["s"]:
                self.camera.setPos(self.camera, Vec3(0, 0.20, 0))
        else:
            if self.d == 1:
             if self.keys["w"] and self.Taste_an:
               self.camera.setPos(self.camera, Vec3(0, 0.003, 0))
             if self.keys["w"] and self.keys["shift"] and self.Taste_an:
               self.camera.setPos(self.camera, Vec3(0, 0.003, 0))
               if hasattr(self, 'Schritte_sound'):
                self.Schritte_sound.setPlayRate(1.95)
             else:
              if hasattr(self, 'Schritte_sound'):
               self.Schritte_sound.setPlayRate(1.0)
            # 💨 Leichte Screen-Vibration beim Sprinten
            #self.camera.setP(self.camera.getP() + (0.05 if int(task.time * 100) % 2 == 0 else -0.1))
            
        
            
              if self.keys["s"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(0, -0.003, 0))
              if self.keys["a"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(-0.003, 0, 0))
              if self.keys["d"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(0.003, 0, 0))
              if self.keys["r"]:
                self.camera.setPos(self.camera, Vec3(0, 0, 0.1))
              if self.camera.getZ() > 1 or self.camera.getZ() < 1:
                self.camera.setZ(1)


        if (self.camera.getX() < -2 or self.camera.getX() > 3) and self.d == 1:
              if self.keys["shift"] and self.keys["w"] :
                self.camera.setPos(self.camera, Vec3(0, -0.20, 0))
              if self.keys["a"]:
                self.camera.setPos(self.camera, Vec3(0.20, 0, 0))
              if self.keys["d"]:
                self.camera.setPos(self.camera, Vec3(-0.20, 0, 0))
              if self.keys["w"] and not self.keys["shift"]:
                self.camera.setPos(self.camera, Vec3(0, -0.20, 0)) 
              if self.keys["s"]:
                self.camera.setPos(self.camera, Vec3(0, 0.20, 0))

        else:
            if self.d == 1:
             if self.keys["w"] and self.Taste_an:
               self.camera.setPos(self.camera, Vec3(0, 0.003, 0))
             if self.keys["w"] and self.keys["shift"] and self.Taste_an:
               self.camera.setPos(self.camera, Vec3(0, 0.003, 0))
               if hasattr(self, 'Schritte_sound'):
                self.Schritte_sound.setPlayRate(1.95)
             else:
              if hasattr(self, 'Schritte_sound'):
               self.Schritte_sound.setPlayRate(1.0)
            # 💨 Leichte Screen-Vibration beim Sprinten
            #self.camera.setP(self.camera.getP() + (0.05 if int(task.time * 100) % 2 == 0 else -0.1))
            
        
            
              if self.keys["s"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(0, -0.003, 0))
              if self.keys["a"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(-0.003, 0, 0))
              if self.keys["d"] and self.Taste_an:
                self.camera.setPos(self.camera, Vec3(0.003, 0, 0))
              if self.keys["r"]:
                self.camera.setPos(self.camera, Vec3(0, 0, 0.1))
            if self.Gravitation == True:
              if self.camera.getZ() > 1 or self.camera.getZ() < 1:
                self.camera.setZ(1)

        if self.e == 1:
           if self.camera.getY() < -29 and self.sound_check13 == False and self.Glitch_Szene == False:
                self.sound_check13 = True
                self.Glitch_Szene = True
                sequence6 = Sequence(
                 Func(self.Glitch_Sfx.play),
                 Wait(0.89),
                 Func(self.setBackgroundColor, 1, 1, 1, 1),
                 Wait(0.1),
                 Func(self.setBackgroundColor, 0, 0, 0, 1),
                 Wait(0.1), 
                 
                    
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    
                    
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.2),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1)
                    
            
                    
                    
                
                )
                    
                 
             
                sequence6.start()


           
          
               
           if not getattr(self, '_dream_transition_scheduled', False) and (
               self.camera.getY() <= -63 
           ):
               self._dream_transition_scheduled = True
               self.taskMgr.doMethodLater(0.1, self.Fade_Out_starten_mit_einem_schwarzen_Overlay, "BlackOverlayTask")
               self.taskMgr.doMethodLater(9, self.Kapitel_4_Video_Starten, "Kapitel2Start")
               self.taskMgr.doMethodLater(43, self.Traum_Szene, "Kapitel2Stop")

            # bewegung in der Kamera während man geht mit import random

               





        return task.cont
            
        #if self.b == 1 and self.Kapitel_1_Auto_kommt_gestartet:
            # Ich werde jetzt hier jetzt das Video 5 einfügen, um den 2 Kapitel einzuleiten, wo der Protagonist im Koma liegt.

            

        


        
      
    def check_interaktion(self, task):
    # 1. Distanz prüfen (ist der Spieler nah genug am Auto?)
      if self.g == 1:
       self.distanz = self.camera.getDistance(self.Auto_Modell3)
    
       if self.distanz < 30: # Nur wenn Spieler nah dran ist
             # 2. Winkel prüfen (schaut er in die Richtung des Autos?)
             # Wir berechnen den Vektor zum Auto
             vektor_zum_auto = self.Auto_Modell3.getPos(self.camera)
             vektor_zum_auto.normalize()
        
             # Die Kamera schaut in Panda3D immer in Richtung der Y-Achse
             # Wir vergleichen, wie weit die Blickrichtung vom Ziel abweicht
             blick_richtung = self.camera.getMat().getRow3(1)
        
             # Dot-Product Ergebnis 1.0 = schaut perfekt drauf
             # Alles über 0.9 ist "nah genug dran"
             if blick_richtung.dot(vektor_zum_auto) > 0.9:
              # HIER ERSCHEINT DEIN "DRÜCKE E" TEXT
                self.zeige_interaktions_text.setText("Drücke E, um das Auto anzusehen")
             else:
                self.zeige_interaktions_text.setText("")
            
       return task.cont
    
    def updater_fpr_sounds(self, task):
        # Bessere Logik: Gruppiere Tastenzustand und Taste_Aktiv-Flag korrekt
        moving = (self.keys["w"] or self.keys["a"] or self.keys["s"] or self.keys["d"]) and self.Taste_an

        # Fußschritte im Spiel-Modus (b == 1)
        if self.f == 1:
            if moving:
                if  self.sound_check9 == False:
                    self.sound_check9 = True
                    self.Schritte_sound = loader.loadSfx(resource_path('sounds/freesoundsxx-walking-on-concrete-ver-2-268513.mp3'))
                    self.Schritte_sound.setLoop(True)
                    self.Schritte_sound.setVolume(1)
                    self.Schritte_sound.play()
            else:
                if self.sound_check9:
                    self.sound_check9 = False
                    if hasattr(self, 'Schritte_sound'):
                        self.Schritte_sound.stop()

        # Fußschritte für andere Szene/Mode (e == 1)
        if self.e == 1:
            moving_e = (self.keys["w"] or self.keys["a"] or self.keys["s"] or self.keys["d"]) and self.Taste_an
            if moving_e:
                if not self.sound_check12:
                    self.sound_check12 = True
                    # Sicherstellen, dass Walking_sound geladen ist
                    if not hasattr(self, 'Walking_sound') or self.Walking_sound is None:
                        self.Walking_sound = loader.loadSfx(resource_path('sounds/Walking.mp3'))
                    self.Walking_sound.setLoop(True)
                    self.Walking_sound.setVolume(1)
                    self.Walking_sound.play()


    
            else:
                if self.sound_check12:
                    self.sound_check12 = False
                    if hasattr(self, 'Walking_sound'):
                        self.Walking_sound.stop()
        if self.g == 1:
            if moving:
                if not self.sound_check14:
                    self.sound_check14 = True
                    self.Schritte_sound5 = loader.loadSfx(resource_path('sounds/jokerzillagames-walking-366933.mp3'))
                    self.Schritte_sound5.setLoop(True)
                    self.Schritte_sound5.setVolume(1)
                    self.Schritte_sound5.play()
            else:
                if self.sound_check14:
                    self.sound_check14 = False
                    if hasattr(self, 'Schritte_sound5'):
                        self.Schritte_sound5.stop()

        
            #Ich werde da gleich was hinzufügen, warte bitte.

        return task.cont
        
    def set_master_volume(self, volume):
      """Setzt die Lautstärke für alle Sounds und Musik (Wert von 0.0 bis 1.0)"""
      # Wichtig: Den Wert explizit als Float übergeben
      v = float(volume)
    
      # Alle SFX-Manager anpassen
      for sfx_mgr in base.sfxManagerList:
        sfx_mgr.set_volume(v)  # <--- Hier von setVolume auf set_volume ändern
      base.musicManager.set_volume(v) 
      
    def update_H_of_camera(self, task):
     
        # Mausbewegung abfragen
        # Nur bewegen, wenn das Spiel aktiv ist (b == 1)
        if self.mouseWatcherNode.hasMouse() and self.b == 1 and self.Taste_an:
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()
            
            # 1. HPR-Werte abrufen
            h = self.camera.getH(render)
            p = self.camera.getP(render)
            r = self.camera.getR(render)
            
            # 2. Heading drehen (DEIN ORIGINALER FAKTOR 100)
            # Reduziere die Deadzone deutlich, um ruckartige Steuerung zu vermeiden
            deadzone = 0.0022
            dx = x if abs(x) > deadzone else 0.0
            dy = y if abs(y) > deadzone else 0.0

            new_h = h - (dx * 100)
            # Pitch anpassen (DEIN ORIGINALER FAKTOR 100)
            new_p = max(-89, min(89, p + (dy * 100)))

            new_r = r * 0.95  # Optional: Roll leicht reduzieren, um Stabilität zu erhöhen

            # 4. Kamera setzen
            if self.RollCamera == True:
              self.camera.setHpr(render, new_h, new_p, new_r)
            else:
                self.camera.setHpr(render, new_h, new_p, 0)  # Roll auf 0 setzen, wenn RollCamera False ist

            # 5. Maus zentrieren nur bei Bewegung außerhalb der Deadzone
            if dx != 0.0 or dy != 0.0:
                props = self.win.getProperties()
                center_x = int(props.getXSize() / 2)
                center_y = int(props.getYSize() / 2)
                self.win.movePointer(0, center_x, center_y)
            
        return task.cont
        
            
    def Glitch(self):
         sequence12 = Sequence(
                 Func(self.Glitch_Sfx.play),
                 Wait(0.89),
                 Func(self.setBackgroundColor, 1, 1, 1, 1),
                 Wait(0.1),
                 Func(self.setBackgroundColor, 0, 0, 0, 1),
                 Wait(0.1), 
                 
                    
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    
                    
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.2),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 1, 1, 1, 1),
                    Wait(0.1),
                    Func(self.setBackgroundColor, 0, 0, 0, 1)
                    
            
                    
                    
                
                )
                    
                 
             
         sequence12.start()
    
    def Pause(self):
        if self.b == 1:  # Einfacher Umschalter: Wenn True, dann False - und umgekehrt
          self.Taste_an = not self.Taste_an
          self.Settings_knopf = True
        
        # Mauszeiger anzeigen/verstecken
          from panda3d.core import WindowProperties
          props = WindowProperties()
          props.setCursorHidden(self.Taste_an) # Wenn Taste_an True ist (Spiel läuft), Maus verstecken
          self.win.requestProperties(props)
        
          if not self.Taste_an:
            print("Spiel pausiert (Steuerung aus)")
          else:
            print("Spiel läuft (Steuerung an)")

          if not self.Taste_an and self.b == 1:
            # Hier kommt mein Video rein, was ein Menü darstellen soll
            self.video_path = resource_path('videos/0607-Kopie-Kopie(1).mp4')
            self.Knopf_bereit_damit_Ui_clickbar_ist_für_pause_menu = True
            self.video3 = MovieTexture("mein_video_loop")
            if self.video3.read(self.video_path):
                          self.video3.setLoopCount(0) 
                
                        # 3. Fullscreen-Fläche für das Video erstellen und an render2d hängen
                          cm = CardMaker("video_plane")
                          cm.setFrame(-1.8, 1.8, -1.8, 1) 
                          self.video_flaeche3 = render2d.attachNewNode(cm.generate())
                          self.video_flaeche3.setPos(0.71, 0, 0.76)
                          
                         
                
                # 4. Video auf die Fläche legen und abspielen
                          self.video_flaeche3.setTexture(self.video3)
                          self.video3.play()
                          self.Night_ambiente.stop()
                          self.Horror_music.stop()
                          self.Humming_sound.play()
                         
                          
                          self.Settings_knopf = True
                        
      

            # In der Update-Schleife für dein Menü:
           
          else:
            if hasattr (self, 'video_flaeche3'):
              self.video_flaeche3.removeNode()
            if self.jumpscare_passiert == False:
                   
                self.Night_ambiente.play()
                self.Horror_music.play()
            self.Knopf_bereit_damit_Ui_clickbar_ist_für_pause_menu = False
            self.Humming_sound.stop()
            if hasattr(self, 'video3'):
                self.video3.stop()
            if hasattr(self, 'video_flaeche4'):
                self.video_flaeche4.removeNode()
            if hasattr(self, 'video4'):
                self.video4.stop()
            if hasattr(self, 'mein_bild2'):
                self.mein_bild2.hide()
            self.zurück_gehen_ist_erlaubt = False
            self.erlaubt_für_Ui_settings = False
            self.Settings_knopf = False
                      # 2. MovieTexture korrekt erstellen und laden
      
        

    def update_mouse_task(self, task):
        if self.mouseWatcherNode.hasMouse():
            # Maus kontinuierlich in der Mitte halten während Spielstart
            if self.b == 1 and self.Taste_an: 
                center_x = int(self.win.getXSize() / 2)
                center_y = int(self.win.getYSize() / 2)
                self.win.movePointer(0, center_x, center_y)
            
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()
            
            #self.maus_anzeige.setText(f"Mouse Position: ({x:.2f}, {y:.2f})")

            # Prüfen, ob die Maus über dem Text "Klicke, um zu beginnen!" schwebt
            if -0.11 < x < 0.10 and -0.73 < y < -0.70 :
                self.beginnen_text.setFg((1, 0, 0, 1))
                def text_wird_größer(alpha):
                    self.beginnen_text.setScale(alpha)

                text_wird_größerr= LerpFunc(
                    text_wird_größer,
                    fromData=0.08,
                    toData=0.05,
                    duration=0.7
                )
                text_wird_größerr.start()
                if not self.hover_sound_gespielt:
                  meine_sound_click = loader.loadSfx(resource_path('sounds/miraclei-sample_hover_subtle04_kofi_by_miraclei-364171.mp3'))
                  meine_sound_click.setVolume(0.3)  
                  meine_sound_click.play()
                
                self.hover_sound_gespielt = True

                
             

                
                # KLICK-ERKENNUNG
                if self.animation_gestartet and self.keys["mouse1"] and not self.ausblenden_gestartet:
                    self.ausblenden_gestartet = True 
                    self.hover_sound_gespielt = True 
                    self.zurück_gehen_ist_erlaubt = False
                    self.video_flaeche2.removeNode()
                    self.mein_bild2.hide()   # Stoppe das Intro-Video
                    if self.Capcut_Scene == False:
                      self.Capcut_Scene = True
                      self.Computer_startet = loader.loadSfx(resource_path('sounds/soundreality-pc-computer-hard-drive-disk-hum-462688.mp3'))
                      self.Computer_startet.play()
                      self.taskMgr.doMethodLater(4.5, lambda task: Video_Intro(self, task), "StartVideoIntroTimer")
                      # 1. Dynamischen Pfad zur AVI-Datei erstellen
                      def Video_Intro(self, task):
                        self.video_path = resource_path('videos/EndProduktFürTeil1.mp4')
                        if hasattr(self, 'video_flaeche3'):
                            self.video_flaeche3.removeNode()
                        # 2. MovieTexture korrekt erstellen und laden
                        self.video = MovieTexture("mein_video_loop")
                        if self.video.read(self.video_path):
                          self.video.setLoopCount(0) 
                
                        # 3. Fullscreen-Fläche für das Video erstellen und an render2d hängen
                          cm = CardMaker("video_plane")
                          cm.setFrame(-1.5, 1.8, -1.2, 1.7) 
                          self.video_flaeche = render2d.attachNewNode(cm.generate())
                          self.video_flaeche.setPos(0.5, 1, 0.16)
                          
                        
                          self.game_startet = True
                          self.mein_bild2.hide()
                         
                
                # 4. Video auf die Fläche legen und abspielen
                          self.video_flaeche.setTexture(self.video)
                          self.video.play()
                          
                          self.Der_SOund_für_die_Szene = loader.loadSfx(resource_path('sounds/EndProduktFürTeil1 Kopie.mp3'))
                          self.Der_SOund_für_die_Szene.play()
                          
                      self.hover_sound.play()
                      self.beginnen_text.setText("") 
                    #self.meine_musik.stop()
                    
                    #self.mein_sound = loader.loadSfx(resource_path('sounds/freesound_community-slot-loading-cd-dvd-drive-spin-up-fail-incl-27275.mp3'))
                    #self.mein_sound.play()
                      self.taskMgr.doMethodLater(4.5, lambda task: sprechen(self, task), "StrtKapitel1Timer")  
                    
                    def sprechen(self, task):
                      self.Speaking_person = loader.loadSfx(resource_path('sounds/audio (online-audio-converter.com).mp3')) 
                      self.Speaking_person.play()
                      self.Computer_startet.setVolume(0.1)  # Computer-Start-Sound leiser machen
                      return task.done
                       
                    self.taskMgr.doMethodLater(55, self.Kapitel_1 , "StartKapitel1Timer")  
                    
            else:
                self.hover_sound_gespielt = False
                sekunden = int(task.time)
                if sekunden > 7:  
                    self.beginnen_text.setFg((1, 1, 1, 1))
        return task.cont
        
    def set_key(self, key, value):
        self.keys[key] = value

    
        

    def Kapitel_1(self, task):
      if self.b == 1:
          self.starte_fade_in(3.0)  # Starte den Fade-In mit einer Dauer von 3 Sekunden
      if hasattr(self, 'video_flaeche'):
        self.video_flaeche.removeNode()
      if hasattr(self, 'Der_SOund_für_die_Szene'):
        self.Der_SOund_für_die_Szene.stop()
      if hasattr(self, 'video'):
        self.video.stop()
      if hasattr(self, 'video2'):
        self.video_flaeche2.removeNode()
        self.video2.stop()
        self.Humming_sound.stop()
      if self.a==1:
        self.Check_for_cordinates = True
      if self.a==1:
        self.b = 1
        self.Night_ambiente = loader.loadSfx(resource_path('sounds/freesound_community-night-ambience-17064.mp3'))
        self.Night_ambiente.setLoop(True)
        self.Night_ambiente.play()
        # Maus direkt zentrieren
        self.Horror_music = loader.loadSfx(resource_path('sounds/universfield-horror-background-atmosphere-025-499631.mp3'))
        self.Horror_music.setLoop(True)
        self.Horror_music.play()
      
          

        
    
      # UI BEHALTEN (timer_text und maus_anzeige sind wichtige Werkzeuge!)
      # Nur den Introtext ausblenden
      self.beginnen_text.detachNode()
      self.Title.detachNode()
      self.Autor.detachNode()

      #Lets_go_home = loader.loadSfx(resource_path('sounds/ElevenLabs_2026-06-15T12_43_30_Max - Elearning and Documentary_pvc_sp100_s50_sb75_v3.mp3'))
      #Lets_go_home.play()
      
      model_path = resource_path('Models/model.glb')
      self.Protagonist_model = loader.loadModel(model_path)
      self.Protagonist_model.reparentTo(render)
      self.Protagonist_model.setPos(-11.2, 1, -10.1)
      self.Protagonist_model.setHpr(0, 0, 180)
      #from panda3d.core import CardMaker, TextureStage
      self.setBackgroundColor(0,0, 0)  # Sky blue

      # PERFORMANCE OPTIMIERUNGEN
      # Reduziere Shadow-Details
      # Keine MSAA für bessere Performance
      
      # LICHTER - MASSIV VERSTÄRKT für Sichtbarkeit
      

      # MODELL LADEN
      model_name = "procedural_city_5.glb"  # GLB direkt! (nicht OBJ)
      model_path = resource_path("Models/procedural_city_5.glb")

      
      # PERFORMANCE: Modell laden und zur Render hinzufügen
      self.city_model = loader.loadModel(model_path)
      print(f"✓ Modell geladen: {model_path}")
      self.city_model.reparentTo(render)
      self.city_model.setP(90)
      print(f"✓ Modell an render angehängt")
      
      # ☀️ BELEUCHTUNGS-LÖSUNG (reduziert für Atmosphäre)
      from panda3d.core import AmbientLight, DirectionalLight, PointLight, Material
      
      # 1. SCHWACHES AMBIENT LIGHT - Basis Dunkelheit
      ambient = AmbientLight('ambient')
      ambient.setColor((0.15, 0.13, 0.1, 1))  # Sehr dunkel
      ambient_node = render.attachNewNode(ambient)
      render.setLight(ambient_node)
      
      # 2. DIRECTIONAL LIGHT - Mondlicht (kühl)
      dlight = DirectionalLight('dlight')
      dlight.setColor((0.25, 0.25, 0.35, 1))  # Schwaches blau-Licht
      dlight_node = render.attachNewNode(dlight)
      dlight_node.setPos(0, 20, 30)
      dlight_node.lookAt(0, 0, 0)
      render.setLight(dlight_node)
      
      # 3. POINT LIGHT - auf Kamera (warm!)
      plight = PointLight('plight')
      plight.setColor((0.8, 0.6, 0.4, 1))  # Warm gelb, aber schwächer
      plight.setAttenuation((1, 0.01, 0.0001))  
      plight_node = render.attachNewNode(plight)
      plight_node.setPos(49, -7.7, 3)
      render.setLight(plight_node)
      print(f"✓ 3-Lichter-System mit schwacher Helligkeit")
      
      # Material - NICHT zu glänzend!
      mat = Material()
      mat.setSpecular((0.1, 0.1, 0.1, 1))  # Sehr wenig Glanz
      mat.setShininess(20.0)
      self.city_model.setMaterial(mat, 1)
      
      # 🔴 SHADER JETZT AKTIVIEREN (nach den Lichtern!)
      render.setShaderAuto()

      



      self.camera.setPos(49, -7.7, 1)
      self.camera.setP(0)
      self.camLens.setFov(80)
      self.camera.setH(0)
      self.camera.setR(0) # Stadtmodell ist um 180 Grad gedreht, also Kamera auch
      self.camera.setZ(1)
      self.camera.setY(-7.7) 

      #if self.b == 1:
          #from direct.filter.FilterManager import FilterManager
          #from panda3d.core import Texture

       # FilterManager für Post-Processing Effekte
          #self.manager = FilterManager(base.win, base.cam)
          #self.blur_tex = Texture()
          # Erstellt eine Fläche, die das aktuelle Bild enthält
          #self.quad = self.manager.renderSceneInto(colortex=self.blur_tex)
          # Wir setzen die Textur auf das Vollbild-Rechteck
          #self.quad.setTexture(self.blur_tex)
          #self.quad.setAlphaScale(0.8)
      
      # 🌑 DUNKLES OVERLAY - An render2d für garantierte Sichtbarkeit
      #from panda3d.core import CardMaker
      #cm = CardMaker("dark_overlay")
      #cm.setFrame(-1.5, 1.5, -1.5, 1.5)
      #self.overlay = render2d.attachNewNode(cm.generate())
      #self.overlay.setPos(0, 0, 0)
      #self.overlay.setColor(0, 0, 0, 0.3)  # 60% Verdunkelung - ändere 0.6 für mehr/weniger
      #self.overlay.setBin("transparent", 30)  # Über allem anderen rendern
      #self.overlay.setDepthTest(False)
      #self.overlay.setDepthWrite(False)
      #print(f"✓ Dunkles Overlay aktiviert auf render2d")
        
        # TEXTUREN AKTIVIEREN! (Wichtig für Wanddetails)
      
        
    
      return task.done
    
      
    def Kapitel_2(self, task):
        # WICHTIG: Nur einmal ausführen!
        if hasattr(self, 'Kapitel_2_aufgerufen'):
            return task.done
        self.Kapitel_2_aufgerufen = True
        
        if hasattr(self, 'Auto_Modell'):
              self.Auto_Modell.removeNode()
              del self.Auto_Modell # Löscht die Referenz komplett

            # Korrektur: Wenn das Modell in self.city_model gespeichert ist, nutze das
        if hasattr(self, 'city_model'):
              self.city_model.removeNode()
              del self.city_model

        self.Horror_ambiente_background.stop()

            # 2. Alle anderen Kinder von render entfernen (Sicherheits-Check)
            # Wir behalten die Kamera!
        for node in render.getChildren():
              if node != self.camera and node.getName() != "camera":
                node.removeNode()

            # 3. Sounds stoppen
        sounds = ['Horror_ambiente_background', 'Horror_music', 'Night_ambiente', 'Humming_sound']
        for s in sounds:
              if hasattr(self, s):
                getattr(self, s).stop()

        self.taskMgr.doMethodLater(5, self.ambulance_kommt, "AmbulanceSoundTimer")
        self.taskMgr.doMethodLater(10, self.Kapitel_2_echter_beginn, "AmbulanceSoundTimer2")
            

        return task.done
            
            
    
    
    
    def ambulance_kommt(self, task):
              if hasattr(self, 'Horror_ambiente_background'):
                self.Horror_ambiente_background.setVolume(0.01)
              self.Ambulance_sound = loader.loadSfx(resource_path('sounds/49053354-ambulance-312230.mp3'))
              self.Ambulance_sound.play()
              self.heart_beat = loader.loadSfx(resource_path('sounds/dragon-studio-heartbeat-sound-372448.mp3'))
              self.heart_beat.play()
              return task.done

    def Kapitel_2_echter_beginn(self, task):
        self.video_path = resource_path('videos/0607-Kopie-Kopie (2)(1).mp4')
        
        self.video7 = MovieTexture("mein_video_loop")
        if self.video7.read(self.video_path):
            self.video7.setLoopCount(0)
            
            cm = CardMaker("video_plane")
            # Kleineres Frame zum Testen
            cm.setFrame(-1.5, 2.2, -1.5, 2.2)
            
            # WICHTIG: aspect2d nutzen
            self.video_flaeche7 = aspect2d.attachNewNode(cm.generate())
            
            # Position direkt hier setzen
            self.video_flaeche7.setPos(0.42, 0, 0.4) 
            
            self.video_flaeche7.setTexture(self.video7)
            self.video7.play()
        
        self.Humming_sound.play()
        self.taskMgr.doMethodLater(29, self.WohnungSzene_starten, "WohnungSceneStartTimer")
        return task.done
    
    def WohnungSzene_starten(self, task):
        if self.b == 1:
            self.d = 1
            
        
        # WICHTIG: Nur einmal ausführen!
        if hasattr(self, 'Wohnung_geladen'):
            return task.done
        self.Wohnung_geladen = True
        
        self.Kapitel_2_beginn = True
        self.Pause()
        
        # 1. Video ausblenden/entfernen
        if hasattr(self, 'video_flaeche7'):
            self.video_flaeche7.removeNode()
        if hasattr(self, 'video7'):
            self.video7.stop()
        
        # 2. Sound stoppen
        if hasattr(self, 'Ambulance_sound'):
            self.Ambulance_sound.stop()
        if hasattr(self, 'heart_beat'):
            self.heart_beat.stop()
        if hasattr(self, 'Humming_sound'):
            self.Humming_sound.stop()
        
        # 3. Texture-Suchpfade konfigurieren (WICHTIG für externe Texturen!)
        from panda3d.core import get_model_path
        texture_path = resource_path('Models/textures')
        get_model_path().append_path(texture_path)
        print(f"Texture-Pfad hinzugefügt: {texture_path}")
        
        # 4. Wohnung laden
        model_path = resource_path('Models/white_modern_living_room.glb')
        self.Wohnung = loader.loadModel(model_path)
        self.Wohnung.reparentTo(render)
        self.Wohnung.setPos(0, 0, 0)
        print(f"✓ Wohnung geladen: {model_path}")
        
        # 5. Texturen explizit neu laden (falls Problem mit Pfaden)
        self.Wohnung.clearColorScale()
        self.Wohnung.setColorScale(1, 1, 1, 1)  # Stellt sicher, dass Farben nicht verfälscht sind
        
        # 6. Lighting aktivieren für bessere Sichtbarkeit der Texturen
        from panda3d.core import AmbientLight, DirectionalLight, PointLight
        # Ambient Light
        ambient = AmbientLight("ambient")
        ambient.setColor((0.6, 0.6, 0.6, 1))
        self.render.attachNewNode(ambient).reparentTo(self.render)
        self.render.setLight(self.render.attachNewNode(ambient))
        
        # Directional Light (Mondlicht-Effekt)
        dlight = DirectionalLight("dlight")
        dlight.setColor((0.5, 0.5, 0.6, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45, -60, 0)
        self.render.setLight(dlnp)
        
        # 7. Kamera für 3D-Szene positionieren
        self.camera.setPos(0, 0, 1.5)
        self.camera.setHpr(0, 0, 0)
        self.camLens.setFov(90)
        
        print(f"✓ Wohnung-Szene gestartet (Kamera: {self.camera.getPos()})")
        self.taskMgr.doMethodLater(3, self.Protagonist_spricht, "ProtagonistSpeakingTimer")

     
        return task.done
    
    def Beenden_Video (self, task):
        if hasattr(self, 'video10'):
            self.video10.stop()
        if hasattr(self, 'video_flaeche10'):
            self.video_flaeche10.removeNode()


    def Task_Anzeige(self):
        self.video_path = resource_path('videos/0607-Kopie-Kopie (3).mp4')
           
        self.video10 = MovieTexture("mein_video_loop")
        if self.video10.read(self.video_path):
                          self.video10.setLoopCount(0) 
                
                        # 3. Fullscreen-Fläche für das Video erstellen und an render2d hängen
                          cm = CardMaker("video_plane")
                          cm.setFrame(-1.8, 1.8, -1.8, 1) 
                          self.video_flaeche10 = render2d.attachNewNode(cm.generate())
                          self.video_flaeche10.setPos(0.71, 0, 0.76)
                          
                         
                
                # 4. Video auf die Fläche legen und abspielen
                          self.video_flaeche10.setTexture(self.video10)
                          self.video10.play()
                          self.taskMgr.doMethodLater(4.8, self.Beenden_Video, "BitteKOl")
        

    def Das_Meeting_startet(self):
        dialogue_sequence3 = Sequence(
            Func(self.Ringtone.play),
            Wait(0.5),
            Func(self.Glitch),
            Wait(6.5),
            Func(self.starte_schreib_animation, " ???: Welcome Mr. Smith, it's good to finally meet you."),
            Func(lambda: setattr(self, 'c', 1)),
            Wait(7.9),
            Func(lambda : setattr(self, 'c', 0)),
            Func(self.starte_schreib_animation, " YOU: Hello Mr. Robinson. I am very happy to be here."),
            Wait(12),
            Func(lambda : setattr(self, 'c', 1)),
            
            Func(self.starte_schreib_animation, " Mr. Robinson: Before we start, i want to say, that i respect your life story and.........................."),
            Wait(15.2),
            Func(self.Fade_Out_starten_mit_einem_schwarzen_Overlay),
            Wait(8),
            Func(self.Kapitel_3_Video_starten, task=None),
            Wait(9.8), 
            Func(self.Kapitel_3_Szene_starten, task=None),
            Wait(2),
            Func(self.Text_für_Kapitel_3_anzeigen, task=None)

        )
        dialogue_sequence3.start()
        
       

        
        

    def Kapitel_3_Szene_starten(self, task):
        self.Taste_an = True

        
        if hasattr(self, 'Wohnung'):
            self.Wohnung.removeNode()
            del self.Wohnung
        if hasattr(self, 'video_flaeche8'):
            self.video_flaeche8.removeNode()
        if hasattr(self, 'video8'):
            self.video8.stop()
        if hasattr(self, 'Humming_sound'):
            self.Humming_sound.stop()
        if hasattr(self, 'video_flaeche7'):
            self.video_flaeche7.removeNode()
        if hasattr(self, 'video7'):
            self.video7.stop()
        if hasattr(self, 'black_overlay'):
            self.black_overlay.removeNode()
            del self.black_overlay
        self.Kapitel_3_beginn = True
        self.d = 0
        self.e = 1
        self.setBackgroundColor(0, 0, 0)
       
        model_path = resource_path('Models/not_really_japanese_themed_pathway.glb')
        
        self.Kapitel_3_Szene = loader.loadModel(model_path)
        self.Kapitel_3_Szene.reparentTo(render)
        
        self.Kapitel_3_Szene.setPos(0, 0, 0)
        self.Kapitel_3_Szene.setHpr(0, 0, 0)

        self.Kopie1 = self.Kapitel_3_Szene.copyTo(render)
        self.Kopie1.setPos(0, -55, 0)
        self.Kopie1.setHpr(0, 0, 0)
          # Overlay wieder transparent setzen
        self.camera.setPos(-0.13, 39.09, 1)
        self.camera.setHpr(-180, 0, 0)
        self.camLens.setFov(90)
        self.f = 0


       
        print(f"✓ Kapitel 3 Szene geladen: {model_path}")
        

    def Fade_Out_starten_mit_einem_schwarzen_Overlay(self, task=None):
        # Schwarzes Overlay erstellen
        from panda3d.core import CardMaker
        cm = CardMaker("black_overlay")
        cm.setFrame(-10, 10, -10, 10)
        self.black_overlay = render2d.attachNewNode(cm.generate())
        self.Lampe_click.play()
        self.black_overlay.setColor(0, 0, 0, 0)  # Startet transparent
        self.black_overlay.setTransparency(True)
        self.black_overlay.setBin("fixed", 30)  # Über allem anderen rendern
        self.black_overlay.setDepthTest(False)
        self.black_overlay.setDepthWrite(False)

        # Store reference to avoid deletion issues during animation
        overlay_ref = self.black_overlay
        
        # Fade-In Animation starten
        def update_alpha(alpha):
            if overlay_ref and overlay_ref.getParent():
                overlay_ref.setColor(0, 0, 0, alpha)
        
        fade_in_interval = LerpFunc(
            update_alpha,
            fromData=0,
            toData=1,
            duration=5.0,
            blendType='easeInOut'
        )
        fade_in_interval.start()






        if task is not None:
            return task.done

    def Kapitel_3_Video_starten(self, task):
        self.video_path = resource_path('videos/0607-Kopie-Kopie (2)-Kopie.mp4')
        
        self.video8 = MovieTexture("mein_video_loop")
        if self.video8.read(self.video_path):
            self.video8.setLoopCount(0)
            
            cm = CardMaker("video_plane")
            # Kleineres Frame zum Testen
            cm.setFrame(-1.5, 2.4, -1.5, 2.2)
            
            # WICHTIG: aspect2d nutzen
            self.video_flaeche8 = aspect2d.attachNewNode(cm.generate())
            
            # Position direkt hier setzen
            self.video_flaeche8.setPos(0.25, 0, 0.4) 
            
            self.video_flaeche8.setTexture(self.video8)
            self.video8.play()
            self.Humming_sound.play()
            #self.Ticking_sound.play()
    
    def Text_für_Kapitel_3_anzeigen(self, task):
        dialogue_sequence4 = Sequence(
            Func(self.starte_schreib_animation, " YOU: To this day i cant believe, that i wanted to kill myself..."),
            
            Wait(11),
            Func(self.starte_schreib_animation, " YOU: I slowly start to think, that the car crash was the key for my recovery..."),
            Wait(11),
            Func(self.starte_schreib_animation, " YOU: Life seems to be a lot more beautiful than i thought..."),
            Wait(11),
            Func(self.starte_schreib_animation, " YOU: But sometimes too beautiful..."))
        
        
        dialogue_sequence4.start()
        
       



    def Protagonist_spricht(self, task):
        dialogue_sequence2 = Sequence(
            Func(self.starte_schreib_animation, " YOU: After 1 year my life has changed so much… "),
            Wait(12),
            Func(self.starte_schreib_animation, " YOU: I will make my parents proud, my dream job is finally in reach..."),
            Wait(12),
            Func(self.starte_schreib_animation, " YOU: Let's just get through this... and wait, wait and wait... "),
            Wait(15),
            Func(self.Das_Meeting_startet)

        )
        dialogue_sequence2.start()

    def Kapitel_4_Video_Starten(self, task):
        if hasattr(self, 'Kapitel_4_Video_started') and self.Kapitel_4_Video_started:
            return task.done
        self.Kapitel_4_Video_started = True
        if hasattr(self, 'black_overlay'):
            self.black_overlay.removeNode()
            del self.black_overlay

        if hasattr(self, 'Kapitel_3_Szene'):
            self.Kapitel_3_Szene.removeNode()
            del self.Kapitel_3_Szene
        if hasattr(self, 'Kopie1'):
            self.Kopie1.removeNode()
            del self.Kopie1
        
        self.video_path = resource_path('videos/0607-Kopie-Kopie (2)(2).mp4')
        
        self.video9 = MovieTexture("mein_video_loop")
        if self.video9.read(self.video_path):
            
            
            cm = CardMaker("video_plane")
            cm.setFrame(-1.5, 2.2, -1.5, 2.2)
            
            self.video_flaeche9 = aspect2d.attachNewNode(cm.generate())
            self.video_flaeche9.setPos(0.4, 0, 0.2) 
            
            self.video_flaeche9.setTexture(self.video9)
            self.video9.play()
            self.Humming_sound.play()
            self.Boom.play()
            self.Taste_an = False
            return task.done
        
    def Dream_play(self):
        if not self.sound_check16:
          self.Dream5.play()
          self.Dream5.setLoop(True)
          self.sound_check16 = True
        


    def Traum_Szene(self, task):    
        if hasattr(self, 'black_overlay'):
            self.black_overlay.setColor(0, 0, 0, 0)
            self.black_overlay.removeNode()
            del self.black_overlay
        if hasattr(self, 'Kapitel_4_Traumszene_started') and self.Kapitel_4_Traumszene_started:
            return task.done
        self.Kapitel_4_Traumszene_started = True
        if hasattr(self, 'video_flaeche8'):
            self.video_flaeche8.removeNode()
        if hasattr(self, 'video8'):
            self.video8.stop()
        if hasattr(self, 'video_flaeche9'):
            self.video_flaeche9.removeNode()
        if hasattr(self, 'video9'):
            self.video9.stop()
        if hasattr(self, 'Humming_sound'):
            self.Humming_sound.stop()
        self.Taste_an = True

        if self.b == 1:
            self.g = 1
            self.e = 0
            print("Die buchstaben wurden umgesetzt")

        model_path12 = resource_path('Models/stylized_eye.glb')
        
        self.Traum_Szene_model = loader.loadModel(model_path12)
        self.Traum_Szene_model.reparentTo(render)
        
        
        self.Traum_Szene_model.setTwoSided(True)
        
        # Position the eye in front of the camera (not 100 units away!)
        self.Traum_Szene_model.setPos(10, 10, 5)
        self.Traum_Szene_model.setScale(1)
        self.Traum_Szene_model.setHpr(150, -20, 0)
        self.Traum_Szene_model.lookAt(self.camera.getPos(render))  # Make the eye look at the camera initially
       

        self.Kopie2 = self.Traum_Szene_model.copyTo(render)
        self.Kopie2.setPos(-10,  -10, 5)
        self.Kopie2.setHpr(287, -20, 0)
        self.Kopie2.lookAt(self.camera.getPos(render))  # Make the copy look at the camera initially
        

        self.Kopie3 = self.Traum_Szene_model.copyTo(render)
        self.Kopie3.setPos(10, -10, 5)
        self.Kopie3.setHpr(0, -20, 0)
        self.Kopie3.lookAt(self.camera.getPos(render))  # Make the copy look at the camera initially

        model_path13 = resource_path('Models/lamp.glb')
        
        self.Traum_Szene_model2 = loader.loadModel(model_path13)
        self.Traum_Szene_model2.reparentTo(render)

        self.Traum_Szene_model2.setTwoSided(True)
        self.Traum_Szene_model2.setPos(8.7, 5, 5)
        self.Traum_Szene_model2.setScale(0.0234)
        self.Traum_Szene_model2.setHpr(0, 0, 0)

        self.Auto_Modell3 = self.Auto_Modell1.copyTo(render)
        self.Auto_Modell3.setPos(20, 4, 20)
        self.Auto_Modell3.setHpr(0, -90, 0)
        self.Auto_Modell3.setScale(0.034)

        model_path14 = resource_path('Models/House.glb')
        
        self.Traum_Szene_model3 = loader.loadModel(model_path14)
        self.Traum_Szene_model3.reparentTo(render)

        self.Traum_Szene_model3.setTwoSided(True)
        self.Traum_Szene_model3.setPos(-10, 10, 20)
        self.Traum_Szene_model3.setScale(0.05)
        self.Traum_Szene_model3.setHpr(0, 0, 0)

        model_path15 = resource_path('Models/modern_dining_room.glb')

        self.Traum_Szene_model4 = loader.loadModel(model_path15)
        self.Traum_Szene_model4.reparentTo(render)

        self.Traum_Szene_model4.setTwoSided(True)
        self.Traum_Szene_model4.setPos(-30, -10, 5)
        self.Traum_Szene_model4.setScale(1)
        self.Traum_Szene_model4.setHpr(120, 0, 0)
    
    

        

        
       


        if self.taskMgr.hasTaskNamed("DreamEyeLookTask"):
            self.taskMgr.remove("DreamEyeLookTask")
        self.taskMgr.add(self.dream_eye_look_task, "DreamEyeLookTask")

        
        self.camera.setPos(0, -5, 1.5)
        self.camera.setHpr(0, 0, 0)
        self.camLens.setFov(90)
        

        print(f"✓ Traum-Szene geladen: {model_path12}")
        self.taskMgr.doMethodLater(1.5, self.Traum_Szene_Dialouge, "DialougefürTraumszene")
    
        return task.done



    def Weißer_Fade_in(self):
        from panda3d.core import CardMaker
        cm = CardMaker("black_overlay")
        cm.setFrame(-10, 10, -10, 10)
        self.black_overlay = render2d.attachNewNode(cm.generate())
        self.Lampe_click.play()
        self.black_overlay.setColor(1, 1, 1, 0)  # Startet transparent
        self.black_overlay.setTransparency(True)
        self.black_overlay.setBin("fixed", 30)  # Über allem anderen rendern
        self.black_overlay.setDepthTest(False)
        self.black_overlay.setDepthWrite(False)

        overlay_ref = self.black_overlay
        
        # Fade-In Animation starten
        def update_alpha(alpha):
            if overlay_ref and overlay_ref.getParent():
                overlay_ref.setColor(1, 1, 1, alpha)
        
        fade_in_interval = LerpFunc(
            update_alpha,
            fromData=0,
            toData=1,
            duration=3,
            blendType='easeInOut'
        )
        fade_in_interval.start()
        self.FlashBang.play()





    def dream_eye_look_task(self, task):
        if hasattr(self, 'Traum_Szene_model') and self.Traum_Szene_model is not None:
            self.Traum_Szene_model.lookAt(self.camera)
        return task.cont
    
    def Bewegen_Lampe(self):
        self.Traum_Szene_model2.setPos(5 , 5, 5)
        self.Traum_Szene_model2.setScale(0.1)

  


    def Das_Ende_Lampe(self, alpha):
        self.Traum_Szene_model2.setScale(alpha)

    def Das_Ende_Lampe2(self, alpha):
        self.Traum_Szene_model2.setPos(alpha, alpha, alpha)
    


    def Start_Das_Ende_Lampe2(self):
        self.Traum_Szene_model2.setPos(0, 5, 5)


    def Start_Das_Ende_Lampe(self):
        self.Lampe_intervall = LerpFunc(
            self.Das_Ende_Lampe,
            fromData=0.1,
            toData=10,
            duration=5
        )
        self.Lampe_intervall.start()
        self.Traum_Szene_model2.setPos(0, 5, 5)
       





    def Traum_Szene_Dialouge(self, task):
        sequence9 = Sequence(
           
            
            Func(self.starte_schreib_animation, " YOU: What the..."),
            Wait(6),
            Func(self.Glitch),
            Wait(4),
            Func(self.starte_schreib_animation, " YOU: The Lamp looks Weird"),
            Wait(12),
            Func(self.starte_schreib_animation, " ... "),
            Wait(4),
            Func(lambda: setattr(self, 'Taste_an', False)),
            Wait(0.1),
            Func(self.Task_Anzeige),
            Wait(5),
            Func(lambda: setattr(self, 'Taste_an', True)),
            Wait(0.1),
            Func(self.starte_schreib_animation, "YOU: I AM NOT AFRAID OF YOU! WHOEVER YOU ARE!!!!! "),
            Wait(11),
            Func(self.starte_schreib_animation, "YOU: I am Dreaming right!? But-t why is there my apartment an---"),
            Wait(5),
            Func(self.Glitch),
            Wait(2.5),
            Func(self.starte_schreib_animation, "YOU: WHAT IS HAPPENING!"),
            Wait(0.1),
            Func(self.Glitch),
            Wait(3),
            Func(self.Bewegen_Lampe),
            Wait(0.3),
            Func(self.starte_schreib_animation, "YOU: WHERE DID THE LAMP GO!!!"),
            Wait(0.1),
            Func(self.Glitch),
            Wait(0.1),
            Func(self.Start_Das_Ende_Lampe),
            Wait(0.1),
            Func(self.Glitch),
            Wait(0.1),
            Func(self.Start_Das_Ende_Lampe2),
            Wait(0.1),
            Func(self.Weißer_Fade_in),
            Wait(0.1),
            Func(self.Glitch),
            Wait(0.1),
            Func(self.Glitch),
            Wait(5.8),
            Func(self.Das_Finale)
            


            



        )
        sequence9.start()
       
        self.Dream5.setLoop(True) 
        self.Dream5.play()





        return task.done
       # Ich will noch eine Atmen Szene einbauen mit einem gruseligem Ambienten Sound und einem Easter Egg z.b die Erfolge usw.

            

    def Das_Finale(self):
        #base_path = os.path.dirname(os.path.abspath(__file__))
        #self.video_path = resource_path('videos/0630-Kopie.mov')
        self.g = 0
        
        #self.video11 = MovieTexture("mein_video_loop")
        #if self.video11.read(self.video_path):
            
            
           # cm = CardMaker("video_plane")
            #cm.setFrame(-1.5, 2.2, -1.5, 2.2)
            
            #self.video_flaeche11 = aspect2d.attachNewNode(cm.generate())
            #self.video_flaeche11.setPos(0.18, 0, 0.2) 
            
            #self.video_flaeche11.setTexture(self.video11)
            #self.video11.play()
        if hasattr(self, 'Dream5'):
                self.Dream5.stop()
        self.Taste_an = False
        self.taskMgr.doMethodLater(5, self.Das_Echte_Final2, "HalloDUGRO")
        
    #def Das_Echte_Final(self, task):
        #Da kommt das FINALE ENDE WO ER SICH UMBRINGT DA ALLES EIN TRAUM WAR

        #if hasattr(self, 'video11'):
            #self.video11.stop()
        #if hasattr(self, 'video_flaeche11'):
            #self.video_flaeche11.removeNode()
        #if hasattr(self, 'black_overlay'):
            #self.black_overlay.removeNode()
        #self.Boom.play()
        #self.Taste_an = False
        #self.setBackgroundColor(0, 0, 0)
        #self.taskMgr.doMethodLater(5, self.Das_Echte_Final2, "HalloDUGRO")

    def Das_Echte_Final2(self, task):
        self.f = 1
        self.Pause()
        #self.Taste_an = False # <------ Wichtige Boolean-Variable, um die Tasteneingabe zu deaktivieren
        self.Gravitation = False # <------ Wichtige Boolean-Variable, um die Gravitation zu deaktivieren
        self.RollCamera = True # <------ Wichtige Boolean-Variable, um die Kamerarotation zu aktivieren
        if hasattr(self, 'video11'):
            self.video11.stop()
        if hasattr(self, 'video_flaeche11'):
            self.video_flaeche11.removeNode()
        
        if hasattr(self, 'Traum_Szene_model2'):
            self.Traum_Szene_model2.setScale(0.0001)
            self.Traum_Szene_model2.removeNode()
           
            del self.Traum_Szene_model2
        if hasattr(self, 'Traum_Szene_model3'):
            self.Traum_Szene_model3.removeNode()
        if hasattr(self, 'Traum_Szene_model4'):
            self.Traum_Szene_model4.removeNode()
        self.Boom.play()
        

        #Kamera Setts

        
        
        
       
        
        
        model_path = resource_path('Models/corridor_hospital_baked_reflections.glb')
        self.Hospital_model = loader.loadModel(model_path)
        self.Hospital_model.reparentTo(render)
        self.Hospital_model.setPos(0, 0, 0)
        self.Hospital_model.setHpr(0, 0, 0)
        self.Hospital_model.setScale(1.2)
        self.camera.setPos(1.19, -8.35, 0)
        self.camera.setHpr(-270, 0, 0)
        self.Taste_an = False
        print(f"✓ Hospital Modell geladen: {model_path}")
        

        self.taskMgr.doMethodLater(2.5, self.Das_Echte_Final3, "HalloDUGRO2")


    def Das_Echte_Final3(self, task):
        self.heart_beat.play()
        self.Hospitel_Sound.play()
        

        self.setBackgroundColor(0, 0, 0)
        self.Atmen_Sound.play()
        self.taskMgr.doMethodLater(7, self.Das_Echte_Final5, "HalloDUGRO4")

    def Das_Echte_Final5(self, task):

        sequence_final = Sequence(
            Func(self.black_overlay.removeNode),
            Wait(0.1),
            Func(self.Door_slam.play),
            Wait(0.1),

            Func(self.starte_schreib_animation, " Doctor: Mr. Smith, you can now leave the hospital. You are lucky to be alive after the accident."),
            Wait(15),
            Func(self.starte_schreib_animation, " YOU: WHERE AM I? WHAT HAPPENED?"),
            Wait(0.1),
            Func(self.Riser.play),
            Wait(2.8),
            Func(self.Fade_Out_starten_mit_einem_schwarzen_Overlay))

        sequence_final.start()
        self.Atmen_Sound.stop()
        self.heart_beat.stop()
        self.Hospitel_Sound.stop()
        self.Musik_Piano.setLoop(True)
        self.Musik_Piano.play()
        self.taskMgr.doMethodLater(26, self.Das_Echte_Final4, "HalloDUGRO3")

    def Das_Echte_Final4(self, task):
        self.setBackgroundColor(0, 0, 0)
        self.video_path = resource_path('videos/0607-Kopie-Kopie (1)-Kopie.mp4')
        
        self.video9 = MovieTexture("mein_video_loop")
        if self.video9.read(self.video_path):
            
            
            cm = CardMaker("video_plane")
            cm.setFrame(-1.5, 2.2, -1.5, 2.2)
            
            self.video_flaeche9 = aspect2d.attachNewNode(cm.generate())
            self.video_flaeche9.setPos(0.4, 0, 0.2) 
            
            self.video_flaeche9.setTexture(self.video9)
            self.video9.play()
            self.Humming_sound.play()
            self.Boom.play()
            self.taskMgr.doMethodLater(34.5, self.Ende, "HalloDUGRO5")

    def Ende(self, task):
        sys.exit()  # Beendet das Spiel
        # Ich habe es geschafft, das Spiel ist fertig und ich bin sehr stolz auf mich. Ich habe so viel gelernt und es hat mir sehr viel Spaß gemacht. Ich hoffe, dass die Spieler das Spiel genießen werden und dass sie die Geschichte und die Atmosphäre genauso spannend finden wie ich. Vielen Dank an alle, die mich unterstützt haben und mir geholfen haben, dieses Projekt zu realisieren.
        
        
       

        
        


            
        

        
        
        
            




            

        
        #Du setzt noch die Position vom UNfall
        
        

        




game = HorrorGame()
game.run()
