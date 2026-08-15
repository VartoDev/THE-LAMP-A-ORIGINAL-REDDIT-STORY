
import sys
import os
from panda3d.core import loadPrcFileData, Vec3
import random


# 1. FENSTER-EINSTELLUNGEN (Für Mac-Stabilität & schwarzen Hintergrund)
loadPrcFileData("", "load-display pandagl")
loadPrcFileData("", "aux-display p3osxdisplay false")
loadPrcFileData("", "win-background-color 0 0 0") 

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
            
        self.game_font1 = self.game_font
        avenir_condensed_path = "/System/Library/Fonts/Avenir Next Condensed.ttc"
        arial_narrow_path = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"
        if os.path.exists(avenir_condensed_path):
            self.game_font1 = loader.loadFont(avenir_condensed_path)
        elif os.path.exists(arial_narrow_path):
            self.game_font1 = loader.loadFont(arial_narrow_path)

        # Tastatur/Maus-Abfrage einrichten
        self.keys = {"mouse1": False, "w": False, "d": False, "s": False, "a": False, "r": False, "shift": False}
        self.accept("mouse1", self.set_key, ["mouse1", True])
        self.accept("mouse1-up", self.set_key, ["mouse1", False])
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

        # Texte erstellen
        self.maus_anzeige = OnscreenText(text="Warte auf Maus...", pos=(0, -0.9), scale=0.05, fg=(1, 1, 1, 1), align=TextNode.ACenter, mayChange=True)
        self.beginnen_text = OnscreenText(text="Klicke, um zu beginnen!", pos=(0, -0.2), scale=0.05, fg=(1, 1, 1, 0), align=TextNode.ACenter, mayChange=True)
        self.Title = OnscreenText(text="The Lamp", pos=(0, 0), scale=0.3, fg=(1, 0, 0, 0), align=TextNode.ACenter, font=self.game_font, mayChange=True)
        self.timer_text = OnscreenText(text="Time passed: 0", pos=(0, 0.8), scale=0.05, fg=(1, 1, 1, 1), align=TextNode.ACenter, mayChange=True)
        self.narrative_text = OnscreenText(text="", pos=(0, 0), scale=0.05, fg=(1, 1, 1, 0), align=TextNode.ACenter, mayChange=True)
        self.Autor = OnscreenText(text="", pos=(0,0), scale=0.2, fg=(1,1,1,1), align=TextNode.ACenter, mayChange=True)
        self.Cordinates_for_camera = OnscreenText(text="", pos=(0, 0.7), scale=0.05, fg=(1, 1, 1, 1), align=TextNode.ACenter, mayChange=True)
        self.Autor.setFont(self.game_font1)
        
        # Schutzschalter für Animationen und Sounds
        self.animation_gestartet = False
        self.ausblenden_gestartet = False
        self.meine_musikspielt = False
        self.hover_sound_gespielt = False  
        self.sound_check = False
        self.Capcut_Scene = False
        self.sound_check9 = False
        self.Check_for_cordinates = False
        self.a = 1 
        self.b = 0
        
        self.animation_gestartet1 = False
        
        # Tasks starten
        self.taskMgr.add(self.update_mouse_task, "UpdateMouseTask")
        self.taskMgr.add(self.time_manager, "TimeManagerTask")
        self.taskMgr.add(self.Vector3_updater_to_player, "MovementTask")
        self.taskMgr.add(self.updater_fpr_sounds, "SoundUpdateTask")
        self.taskMgr.add(self.update_H_of_camera, "CameraUpdateTask")
        

      
       
        
    def time_manager(self, task):
        sekunden = int(task.time)
        self.timer_text.setText(f"Time passed: {sekunden}")
        
        if sekunden > 1 and not self.animation_gestartet1:
            self.animation_gestartet1 = True 
            
            
            

            self.Autor.setText("A Psychological Horror Game by Varto")
            self.Autor.setScale(0.1)
            self.Autor.setFont(self.game_font)
            if not self.sound_check:
                self.sound_check = True
                self.Sound_Lampe = loader.loadSfx("sounds/dragon-studio-light-switch-382712.mp3")
                self.Sound_Lampe.play()

        if sekunden == 3:
            self.Autor.setFg((1,1,1,1))

            def Autor_ausblenden(alpha):
                self.Autor.setFg((1,1,1,alpha))

            self.Autor_ausblenden_Text = LerpFunc(
                Autor_ausblenden,
                fromData=1.0,
                toData=0.0,
                duration=1.7
            )
            self.Autor_ausblenden_Text.start()

        if sekunden > 5 and not self.animation_gestartet:
            self.animation_gestartet = True  
            
            self.meine_musik = loader.loadSfx("music/logicallism-renovation-407795.mp3")
            if not self.meine_musikspielt:
                self.meine_musikspielt = True
                self.meine_musik.play()
              
            def set_text_alpha(alpha):
                self.Title.setFg((1, 0, 0, alpha))
        
            self.title_fade = LerpFunc(
                set_text_alpha,    
                fromData=0.0,      
                toData=1.0,        
                duration=5     
            )
            self.title_fade.start()
            
            def set_textt_alpha(alpha):
                self.beginnen_text.setFg((1, 1, 1, alpha))
            
            self.beginnen_text_fade = LerpFunc(
                set_textt_alpha,    
                fromData=0.0,      
                toData=1.0,        
                duration=2      
            )
            self.beginnen_text_fade.start()
        if self.Check_for_cordinates:

              Mensch_pos = self.camera.getPos()
              self.Cordinates_for_camera.setText(f"Camera Position: ({Mensch_pos.x:.2f}, {Mensch_pos.y:.2f}, {Mensch_pos.z:.2f})")
         
        return task.cont
    
    def Vector3_updater_to_player(self, task):
        # Wir bewegen die Kamera relativ zu sich selbst
        if self.keys["w"]:
            self.camera.setPos(self.camera, Vec3(0, 0.05, 0))
        if self.keys["w"] and self.keys["shift"]:
            self.camera.setPos(self.camera, Vec3(0, 0.07, 0))
            if hasattr(self, 'Schritte_sound'):
              self.Schritte_sound.setPlayRate(1.95) #  # Schneller laufen mit Shift
            
        else:
            if hasattr(self, 'Schritte_sound'):
              self.Schritte_sound.setPlayRate(1.0)  # Normale Geschwindigkeit
        if self.keys["s"]:
            self.camera.setPos(self.camera, Vec3(0, -0.05, 0))
        if self.keys["a"]:
            self.camera.setPos(self.camera, Vec3(-0.05, 0, 0))
        if self.keys["d"]:
            self.camera.setPos(self.camera, Vec3(0.05, 0, 0))
        if self.keys["r"]:
            self.camera.setPos(self.camera, Vec3(0, 0, 0.1))
        if self.camera.getZ() > 1 or self.camera.getZ() < 1:
            self.camera.setZ(1)  # Maximalhöhe begrenzen
            
        return task.cont
    
    def updater_fpr_sounds(self, task):
        if self.keys["w"] or self.keys["a"] or self.keys["s"] or self.keys["d"]:
            if not self.sound_check9:
                self.sound_check9 = True
                self.Schritte_sound = loader.loadSfx("sounds/freesoundsxx-walking-on-concrete-ver-2-268513.mp3")
                self.Schritte_sound.setLoop(True)
                self.Schritte_sound.play()
        else:
            if self.sound_check9:
                self.sound_check9 = False
                if hasattr(self, 'Schritte_sound'):
                    self.Schritte_sound.stop()
        return task.cont
        
    def update_H_of_camera(self, task):
        if self.mouseWatcherNode.hasMouse() and self.b == 1:
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()
            
            # 1. HPR-Werte im globalen 'render' Raum abrufen
            # Das verhindert, dass Rotationen vom gedrehten Stadt-Modell vererbt werden
            h = self.camera.getH(render)
            p = self.camera.getP(render)
            
            # 2. Heading drehen (um die globale Z-Achse)
            new_h = h - (x * 100)
            
            # 3. Pitch anpassen (zwischen -89 und 89 Grad, um Gimbal Lock zu vermeiden)
            # Da wir die Stadt um 90 Grad gedreht haben, ist Pitch 0 jetzt dein Blick auf die Stadt
            new_p = max(-89, min(89, p + (y * 100)))
            
            # 4. Kamera im globalen Raum setzen
            # WICHTIG: Das R (Roll) erzwingen wir auf 0, um das "Eiern" zu stoppen
            self.camera.setHpr(render, new_h, new_p, 0)
            
            # 5. Maus zentrieren
            self.win.movePointer(0, int(self.win.getXSize() / 2), int(self.win.getYSize() / 2))
            
        return task.cont
            
        return task.cont
    
       
      
        

    def update_mouse_task(self, task):
        if self.mouseWatcherNode.hasMouse():
            # Maus kontinuierlich in der Mitte halten während Spielstart
            if self.b == 1:
                center_x = int(self.win.getXSize() / 2)
                center_y = int(self.win.getYSize() / 2)
                self.win.movePointer(0, center_x, center_y)
            
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()
            
            self.maus_anzeige.setText(f"Mouse Position: ({x:.2f}, {y:.2f})")

            # Prüfen, ob die Maus über dem Text "Klicke, um zu beginnen!" schwebt
            if -0.19 < x < 0.20 and -0.21 < y < -0.16:
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

                meine_sound_click = loader.loadSfx("sounds/miraclei-sample_hover_subtle04_kofi_by_miraclei-364171.mp3")
                meine_sound_click.setVolume(0.3)  
                meine_sound_click.play()
                
                self.hover_sound_gespielt = True

                
                # KLICK-ERKENNUNG
                if self.animation_gestartet and self.keys["mouse1"] and not self.ausblenden_gestartet:
                    self.ausblenden_gestartet = True  
                    if self.Capcut_Scene == False:
                      self.Capcut_Scene = True
                      # 1. Dynamischen Pfad zur AVI-Datei erstellen
                      base_path = os.path.dirname(os.path.abspath(__file__))
                      self.video_path = os.path.join(base_path, "videos", "EndProduktFürTeil1.mov")
            
                      # 2. MovieTexture korrekt erstellen und laden
                      self.video = MovieTexture("mein_video_loop")
                      if self.video.read(self.video_path):
                        self.video.setLoopCount(0) 
                
                      # 3. Fullscreen-Fläche für das Video erstellen und an render2d hängen
                        cm = CardMaker("video_plane")
                        cm.setFrame(1, -1, 1, -1) 
                        self.video_flaeche = render2d.attachNewNode(cm.generate())
                
                # 4. Video auf die Fläche legen und abspielen
                    self.video_flaeche.setTexture(self.video)
                    self.video.play()

                    def fade_out_text1(alpha):
                        self.Title.setFg((1, 0, 0, alpha))
                    
                    self.title_fade_out = LerpFunc(
                        fade_out_text1,
                        fromData=1.0,
                        toData=0.0,
                        duration=3
                    )
                    self.title_fade_out.start()
                    self.beginnen_text.setText("") 
                    self.meine_musik.stop()
                    
                    #self.mein_sound = loader.loadSfx("sounds/freesound_community-slot-loading-cd-dvd-drive-spin-up-fail-incl-27275.mp3")
                    #self.mein_sound.play()
                    self.taskMgr.doMethodLater(1.9, lambda task: sprechen(self, task), "StrtKapitel1Timer")  
                    
                    def sprechen(self, task):
                       #self.Speaking_person = loader.loadSfx("sounds/audio (online-audio-converter.com).mp3") 
                       #self.Speaking_person.play()
                       return task.done
                       
                    self.taskMgr.doMethodLater(44, self.Kapitel_1 , "StartKapitel1Timer")  
            else:
                self.hover_sound_gespielt = False
                sekunden = int(task.time)
                if sekunden > 7:  
                    self.beginnen_text.setFg((1, 1, 1, 1))
        return task.cont
        
    def set_key(self, key, value):
        self.keys[key] = value

    
        

    def Kapitel_1(self, task):
      if hasattr(self, 'video_flaeche'):
        self.video_flaeche.removeNode()
      if hasattr(self, 'video'):
        self.video.stop()
      if self.a==1:
        self.Check_for_cordinates = True
      if self.a==1:
        self.b = 1
        Night_ambiente = loader.loadSfx("sounds/freesound_community-night-ambience-17064.mp3")
        Night_ambiente.setLoop(True)
        Night_ambiente.play()
        # Maus direkt zentrieren
        
        
        
    

      # UI BEHALTEN (timer_text und maus_anzeige sind wichtige Werkzeuge!)
      # Nur den Introtext ausblenden
      self.beginnen_text.detachNode()
      self.Title.detachNode()
      self.Autor.detachNode()
      
      base_path = os.path.dirname(os.path.abspath(__file__))
      model_path = os.path.join(base_path, "Models", "model.glb")
      self.Protagonist_model = loader.loadModel(model_path)
      self.Protagonist_model.reparentTo(render)
      self.Protagonist_model.setPos(-11.2, 1, -10.1)
      self.Protagonist_model.setHpr(0, 0, 180)
      #from panda3d.core import CardMaker, TextureStage
      #base_path = os.path.dirname(os.path.abspath(__file__))
      #img_path = os.path.join(base_path, "photos", "pexels-stars-1869447_1920.jpg")
      #my_texture = loader.loadTexture(img_path)

      # 2. Eine Karte (Quad) im 3D-Raum erstellen
      #cm = CardMaker("background_card")
      #cm.setFrame(-500, 500, -500, 500) # Sehr groß, damit es alles abdeckt
      #self.background_node = render.attachNewNode(cm.generate())

      # 3. Bild auf die Karte legen
      #self.background_node.setTexture(my_texture)

      # 4. WICHTIG: Das Bild hinter die Stadt schieben
      #self.background_node.setPos(0, 800, 0) # Weit weg nach hinten
      #self.background_node.setBin('background', 1)
      #self.background_node.setDepthWrite(0) # Nicht in die Z-Buffer schreiben
      #self.background_node.setLightOff()    # Beleuchtung ignorieren, sonst ist es zu dunkel

          
          
      # BLAUER HIMMEL für die Stadt
      self.setBackgroundColor(0,0, 0)  # Sky blue

      # PERFORMANCE OPTIMIERUNGEN
      # Reduziere Shadow-Details
      render.setShaderInput("msaa_samples", 0)  # Keine MSAA für bessere Performance
      
      # LICHTER - BALANCED (Nicht zu hell, nicht zu dunkel)
      from panda3d.core import AmbientLight, DirectionalLight
      ambient_light = AmbientLight("ambient_light")
      ambient_light.setColor((0.3, 0.3, 0.3, 1))  # Weiches Umgebungslicht
      ambient_light_node = render.attachNewNode(ambient_light)
      render.setLight(ambient_light_node)
      directional_light = DirectionalLight("directional_light")
      directional_light.setColor((0.7, 0.7, 0.7
     , 1))  # Helleres gerichtetes Licht
      directional_light_node = render.attachNewNode(directional_light)
      directional_light_node.setHpr(45, -60, 0)  # Licht von schräg oben
      render.setLight(directional_light_node)

      # MODELL LADEN
      base_path = os.path.dirname(os.path.abspath(__file__))
      model_name = "procedural_city_5.glb"  # GLB direkt! (nicht OBJ)
      model_path = os.path.join(base_path, "Models", "procedural_city_5.glb", model_name)

      
      # PERFORMANCE: Flattenlight auf großem Modell
      self.city_model = loader.loadModel(model_path)
      self.city_model.reparentTo(render)
      self.city_model.setP(90)  # Korrekte Ausrichtung

      self.camera.setPos(-10, 2, -107)
      self.camera.setP(0)
      self.camera.setH(0)
      self.camera.setR(0) # Stadtmodell ist um 180 Grad gedreht, also Kamera auch
      self.camera.setZ(2)
      self.camera.setY(2) 
      
      
        # TEXTUREN AKTIVIEREN! (Wichtig für Wanddetails)
        # setShaderOff() war das Problem - Texturen brauchen Shader!
        
        
    
      return task.done
    
      
      

# Das Spiel starten
game = HorrorGame()
game.run()