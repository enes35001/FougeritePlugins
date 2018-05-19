__title__ = 'AntiWallLoot'
__author__ = 'Jakkee'
__version__ = '1.0.1'

import clr
clr.AddReferenceByPartialName("Fougerite", "UnityEngine")
import Fougerite
import UnityEngine


class AntiWallLoot:
    def On_PluginInit(self):
        Util.ConsoleLog(__title__ + " by " + __author__ + " Version: " + __version__ + " loaded.", False)

    def On_LootUse(self, LootStartEvent):
        if LootStartEvent.IsObject:
			ray = Util.GetEyesRay(LootStartEvent.Player)
			ray.direction.x - 0.03
			ray.direction.z - 0.03
			cast = Physics.RaycastAll(ray, 20)
			hits = 0
			lookingatbox = False
			for hit in cast:
				name = hit.collider.gameObject.Name.ToLower()
				#DEBUG LINE BELOW
				Util.log("Found gameObject: " + name)
				#END OF DEBUG
				if name.Contains("woodbox"):
					lookingatbox = True
					continue
				if name.Contains("pillar") or name.Contains("doorframe") or name.Contains("wall"):
					hits =+ 1
			if not lookingatbox:
				LootStartEvent.Cancel()
				LootStartEvent.Player.Message("You are not looking at a chest!")
				return
			elif hits >= 1 and lookingatbox:
				#DEBUG LINE BELOW
				Util.Log("Found " + str(hits) + " objects in the way of chest, Kicking player...")
				#END OF DEBUG
				LootStartEvent.Cancel()
				Util.Log("AntiCrackLoot: " + LootStartEvent.Player.Name + " has been kicked for crack looting!")
				LootStartEvent.Player.Character.netUser.Kick(NetError.Facepunch_Kick_Violation, True)
				
            
