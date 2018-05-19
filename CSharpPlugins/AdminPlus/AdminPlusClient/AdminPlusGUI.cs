using Facepunch;
using RustBuster2016.API;
using System;
using System.Collections.Generic;
using System.Text;
using UnityEngine;

namespace AdminPlus
{
    public class AdminPlusGUI : UnityEngine.MonoBehaviour
    {
        private AdminPlusItemList list = new AdminPlusItemList();

        //Menu settings
        private GUIStyle guiStyle = new GUIStyle();
        internal int Selected = 0;
        internal string[] toolbar = new string[] { "Clothing", "Medical", "Weapons", "Construction", "Resources", "Tools", "Misc" };
        internal Vector2 scrollposition;
        internal Vector2 scrollposition0;
        internal bool PlayerSelector = false;
        internal bool SelectedPlayer = false;
        public bool IsAlive = false;
        //private bool AlwaysAtWorkbench = false;

        //ESP Stuff
        internal bool ESPoptions = false;
        internal bool ESPPlayers = false;
        internal bool ESPSleepers = false;
        internal bool ESPLootables = false;
        internal bool ESPAnimals = false;
        internal bool ESPOres = false;
        internal bool ESPBases = false;

        //NoClip Settings
        internal bool NoClip = false;
        internal bool NoClip_Doors = false;
        internal bool NoClip_WindowBars = false;
        internal bool NoClip_Doorway = false;
        internal bool NoClip_Ceiling = false;
        internal bool NoClip_Foundation = false;
        internal bool NoClip_Wall = false;
        internal bool NoClip_Pillar = false;
        internal bool NoClip_Ramp = false;
        internal bool NoClip_Stairs = false;
        internal bool NoClip_Window = false;
        internal bool NoClip_WoodGate = false;
        internal bool NoClip_LargeSpike = false;
        internal bool NoClip_Barricade = false;
        internal bool NoClip_Shelter = false;
        internal bool NoClip_SmallSpike = false;

        //idk?
        internal bool AdminDoors = false;
        internal bool AdminDestroy = false;
        internal float SpeedLevel = 0f;
        internal float JumpHeight = 0f;

        //Give menu
        internal float AmountToGive = 1;
        internal int ItemToGive = -1;
        internal bool GiveItemMenu = false;

        //Selected player stuff
        internal string LookupName = null;
        internal string LookupHWID = null;
        internal string NewDisplayName = null;
        internal bool Fly = false;
        internal bool Ban = false;
        internal bool Kick = false;


        //Default values
        internal float ServerTime = 8f;
        internal GUIContent[] ItemTextures_Clothing;
        internal GUIContent[] ItemTextures_Medical;
        internal GUIContent[] ItemTextures_Weapons;
        internal GUIContent[] ItemTextures_Construction;
        internal GUIContent[] ItemTextures_Resource;
        internal GUIContent[] ItemTextures_Tools;
        internal GUIContent[] ItemTextures_Misc;
        public Character character;

        //Window Rects
        Rect menuwindow = new Rect(20, 40, Screen.width / 7, 420);
        Rect espwindow = new Rect((Screen.width / 7) + 30, 40, 150, 180);
        Rect noclipwindow = new Rect((Screen.width / 7) + 30, 40, 150, 370);
        Rect editorwindow = new Rect((Screen.width / 7) + 30, 40, Screen.width / 3, Screen.height - 60);
        Rect playerwindow = new Rect((Screen.width / 7) + 30, 40, Screen.width / 5, Screen.height / 2);
        Rect givewindow = new Rect((Screen.width / 7) + 30, 40, (Screen.width - (Screen.width / 7)) - 80, Screen.height - 60);

        public void Start()
        {
            List<GUIContent> Clothing = new List<GUIContent>();
            List<GUIContent> Medical = new List<GUIContent>();
            List<GUIContent> Weapons = new List<GUIContent>();
            List<GUIContent> Construction = new List<GUIContent>();
            List<GUIContent> Resource = new List<GUIContent>();
            List<GUIContent> Tools = new List<GUIContent>();
            List<GUIContent> Misc = new List<GUIContent>();
            foreach (ItemDataBlock item in Bundling.LoadAll<ItemDataBlock>())
            {
                if (list.ItemList.Contains(item.name))
                {
                    if (list.Clothing.Contains(item.name))
                    {
                        Clothing.Add(new GUIContent
                        {
                            image = item.GetIconTexture(),
                            text = item.name,
                            tooltip = item.name
                        });
                    }
                    else if (list.Construction.Contains(item.name))
                    {
                        Construction.Add(new GUIContent
                        {
                            image = item.GetIconTexture(),
                            text = item.name,
                            tooltip = item.name
                        });
                    }
                    else if (list.Medical.Contains(item.name))
                    {
                        Medical.Add(new GUIContent
                        {
                            image = item.GetIconTexture(),
                            text = item.name,
                            tooltip = item.name
                        });
                    }
                    else if (list.Misc.Contains(item.name))
                    {
                        Misc.Add(new GUIContent
                        {
                            image = item.GetIconTexture(),
                            text = item.name,
                            tooltip = item.name
                        });
                    }
                    else if (list.Resources.Contains(item.name))
                    {
                        Resource.Add(new GUIContent
                        {
                            image = item.GetIconTexture(),
                            text = item.name,
                            tooltip = item.name
                        });
                    }
                    else if (list.Tools.Contains(item.name))
                    {
                        Tools.Add(new GUIContent
                        {
                            image = item.GetIconTexture(),
                            text = item.name,
                            tooltip = item.name
                        });
                    }
                    else if (list.Weapons.Contains(item.name))
                    {
                        Weapons.Add(new GUIContent
                        {
                            image = item.GetIconTexture(),
                            text = item.name,
                            tooltip = item.name
                        });
                    }
                    else
                    {
                        continue;
                    }
                }
            }
            ItemTextures_Weapons = Weapons.ToArray();
            ItemTextures_Construction = Construction.ToArray();
            ItemTextures_Clothing = Clothing.ToArray();
            ItemTextures_Medical = Medical.ToArray();
            ItemTextures_Resource = Resource.ToArray();
            ItemTextures_Misc = Misc.ToArray();
            ItemTextures_Tools = Tools.ToArray();

            InvokeRepeating("NoClipSetter", 0f, 0.5f);
        }

        public void Update()
        {
            try
            {
                character = Hooks.LocalPlayer?.controllable?.GetComponent<Character>() ?? null;
                if (character != null)
                {
                    IsAlive = character.alive;

                }

                if (AdminPlus.IsAllowed)
                {
                    if (!ChatUI.IsVisible() && !ConsoleWindow.IsVisible() && !MainMenu.IsVisible() && Input.GetKeyDown(KeyCode.BackQuote))
                    {
                        AdminPlus.Enabled = !AdminPlus.Enabled;
                        Screen.lockCursor = !AdminPlus.Enabled;
                    }

                    if (IsAlive)
                    {
                        //-- Speed / Jump hack --
                        character.ccmotor.jumping.setup.baseHeight = 1f + JumpHeight;
                        character.ccmotor.movement.setup.maxForwardSpeed = 4f + SpeedLevel;
                        character.ccmotor.movement.setup.maxSidewaysSpeed = 4f + SpeedLevel;
                        character.ccmotor.movement.setup.maxBackwardsSpeed = 3f + SpeedLevel;
                        character.ccmotor.movement.setup.maxAirAcceleration = 20f + SpeedLevel;
                        //----------------

                        if (Fly)
                        {
                            var LocalController = PlayerClient.GetLocalPlayer().controllable.GetComponent<HumanController>();
                            var LocalPlayerClient = PlayerClient.GetLocalPlayer().controllable.GetComponent<PlayerClient>();

                            CCMotor ccmotor = LocalController.ccmotor;
                            ccmotor.velocity = Vector3.zero;
                            Angle2 eyesAngles = character.eyesAngles;
                            Vector3 forward = eyesAngles.forward;
                            Vector3 back = eyesAngles.back;
                            Vector3 right = eyesAngles.right;
                            Vector3 left = eyesAngles.left;
                            Vector3 up = eyesAngles.up;
                            if (!ChatUI.IsVisible() && !ConsoleWindow.IsVisible() && !MainMenu.IsVisible())
                            {
                                if (Input.GetKey(KeyCode.W))
                                {
                                    if (Input.GetKey(KeyCode.LeftShift))
                                    {
                                        ccmotor.velocity = ccmotor.velocity + forward * (ccmotor.movement.setup.maxForwardSpeed * 20f);
                                    }
                                    else
                                    {
                                        ccmotor.velocity = ccmotor.velocity + forward * (ccmotor.movement.setup.maxForwardSpeed * 5f);
                                    }
                                }
                                if (Input.GetKey(KeyCode.S))
                                {
                                    if (Input.GetKey(KeyCode.LeftShift))
                                    {
                                        ccmotor.velocity = ccmotor.velocity + back * (ccmotor.movement.setup.maxBackwardsSpeed * 20f);
                                    }
                                    else
                                    {
                                        ccmotor.velocity = ccmotor.velocity + back * (ccmotor.movement.setup.maxBackwardsSpeed * 5f);
                                    }
                                }
                                if (Input.GetKey(KeyCode.A))
                                {
                                    if (Input.GetKey(KeyCode.LeftShift))
                                    {
                                        ccmotor.velocity = ccmotor.velocity + left * (ccmotor.movement.setup.maxSidewaysSpeed * 20f);
                                    }
                                    else
                                    {
                                        ccmotor.velocity = ccmotor.velocity + left * (ccmotor.movement.setup.maxSidewaysSpeed * 5f);
                                    }
                                }
                                if (Input.GetKey(KeyCode.D))
                                {
                                    if (Input.GetKey(KeyCode.LeftShift))
                                    {
                                        ccmotor.velocity = ccmotor.velocity + right * (ccmotor.movement.setup.maxSidewaysSpeed * 20f);
                                    }
                                    else
                                    {
                                        ccmotor.velocity = ccmotor.velocity + right * (ccmotor.movement.setup.maxSidewaysSpeed * 5f);
                                    }
                                }
                                if (Input.GetKey(KeyCode.Space))
                                {
                                    if (Input.GetKey(KeyCode.LeftShift))
                                    {
                                        ccmotor.velocity = ccmotor.velocity + up * (ccmotor.movement.setup.maxSidewaysSpeed * 10f);
                                    }
                                    else
                                    {
                                        ccmotor.velocity = ccmotor.velocity + up * (ccmotor.movement.setup.maxSidewaysSpeed * 4f);
                                    }
                                }
                            }
                            if (ccmotor.velocity == Vector3.zero)
                            {
                                ccmotor.velocity = ccmotor.velocity + Vector3.up * (float)((double)ccmotor.settings.gravity * (double)Time.deltaTime * 0.5);
                            }
                        }
                    }
                }
            }
            catch
            {

            }
        }

        // ADMIN ONLY STUFF BELOW

        private void OnGUI()
        {
            if (AdminPlus.IsAllowed)
            {
                if (IsAlive)
                {
                    if (GUI.Button(new Rect(5, 5, 80, 20), "Admin"))
                    {
                        AdminPlus.Enabled = !AdminPlus.Enabled;
                        if (!ChatUI.IsVisible() && !ConsoleWindow.IsVisible() && !MainMenu.IsVisible())
                        {
                            Screen.lockCursor = !AdminPlus.Enabled;
                        }
                    }

                    if (AdminPlus.Enabled)
                    {
                        GUILayout.Window(0, menuwindow, Menu, "AdminPlus V" + AdminPlus.Instance.Version);
                        if (PlayerSelector)
                        {
                            GUILayout.Window(1, editorwindow, PlayerEditorWindow, "Select a player from the list to lookup");
                        }

                        if (ESPoptions)
                        {
                            GUILayout.Window(2, espwindow, ESP, "ESP Options");
                        }

                        if (NoClip)
                        {
                            GUILayout.Window(3, noclipwindow, NoClipMenu, "NoClip Options");
                        }

                        if (SelectedPlayer)
                        {
                            GUILayout.Window(34, playerwindow, PlayerMenu, "Looking up: " + LookupName);
                        }

                        if (GiveItemMenu)
                        {
                            GUILayout.Window(5, givewindow, GiveScreen, "Give " + LookupName + " an item, Maybe some C4?");
                        }
                    }

                    if (ESPPlayers || ESPAnimals)
                    {
                        foreach (UnityEngine.Object GameObject in FindObjectsOfType(typeof(Character)))
                        {
                            if (GameObject != null)
                            {
                                var Character = GameObject as Character;

                                if (ESPPlayers)
                                {
                                    PlayerClient playerClient = Character?.playerClient ?? null;
                                    if (playerClient != null && playerClient.gameObject != this)
                                    {
                                        DrawLabel(Character.origin, playerClient.userName, Color.blue);
                                    }
                                }

                                if (ESPAnimals)
                                {
                                    string distance = String.Format("{0:0}", Vector3.Distance(Character.transform.position,
                                    character.transform.position));
                                    switch (Character.name.Replace("(Clone)", ""))
                                    {
                                        case "MutantBear":
                                            DrawLabel(Character.origin,
                                                String.Format("Mutant Bear [{0}]", distance, Color.yellow));
                                            break;

                                        case "MutantWolf":
                                            DrawLabel(Character.origin,
                                                String.Format("Mutant Wolf [{0}]", distance, Color.yellow));
                                            break;

                                        case "Chicken_A":
                                            DrawLabel(Character.origin,
                                                String.Format("Chicken [{0}]", distance, Color.yellow));
                                            break;

                                        case "Rabbit_A":
                                            DrawLabel(Character.origin,
                                                String.Format("Rabbit [{0}]", distance, Color.yellow));
                                            break;

                                        case "Stag_A":
                                            DrawLabel(Character.origin,
                                                String.Format("Deer [{0}]", distance, Color.yellow));
                                            break;

                                        case "Bear":
                                            DrawLabel(Character.origin,
                                                String.Format("Bear [{0}]", distance, Color.yellow));
                                            break;

                                        case "Wolf":
                                            DrawLabel(Character.origin,
                                                String.Format("Wolf [{0}]", distance, Color.yellow));
                                            break;

                                        case "Boar_A":
                                            DrawLabel(Character.origin,
                                                String.Format("Boar [{0}]", distance, Color.yellow));
                                            break;

                                    }
                                }
                            }
                        }
                    }

                    if (ESPBases)
                    {
                        foreach (StructureMaster structureMaster in Resources.FindObjectsOfTypeAll(typeof(StructureMaster)))
                        {
                            if (structureMaster != null)
                            {
                                Vector3 pos = structureMaster.transform.position;
                                pos.y = pos.y + 5;
                                string distance = String.Format("{0:0}", Vector3.Distance(pos, character.transform.position));

                                if (structureMaster.gameObject != this)
                                {
                                    DrawLabel(structureMaster.transform.position, String.Format("{0} [{1}]", structureMaster.ownerID.ToString(), distance));
                                }
                            }
                        }
                    }

                    if (ESPLootables)
                    {
                        foreach (UnityEngine.Object GameObject in FindObjectsOfType(typeof(LootableObject)))
                        {

                            if (GameObject != null)
                            {
                                var lootableObject = GameObject as LootableObject;

                                string distance = String.Format("{0:0}", Vector3.Distance(lootableObject.transform.position, character.transform.position));
                                if (lootableObject.gameObject != this)
                                {
                                    DrawLabel(lootableObject.transform.position, String.Format("{0} [{1}]", lootableObject.name.Replace("(Clone)", ""), distance));
                                }
                            }
                        }

                    }

                    if (ESPSleepers)
                    {
                        foreach (UnityEngine.Object GameObject in FindObjectsOfType(typeof(SleepingAvatar)))
                        {

                            if (GameObject != null)
                            {
                                var sleepingAvatar = GameObject as SleepingAvatar;

                                string distance = String.Format("{0:0}", Vector3.Distance(sleepingAvatar.transform.position, character.transform.position));
                                if (sleepingAvatar.gameObject != this)
                                {
                                    DrawLabel(sleepingAvatar.transform.position, String.Format("{0} [{1}]", sleepingAvatar.name.Replace("(Clone)", ""), distance));
                                }
                            }
                        }
                    }

                    if (ESPOres)
                    {
                        foreach (UnityEngine.Object GameObject in FindObjectsOfType(typeof(ResourceObject)))
                        {
                            if (GameObject != null)
                            {
                                var resourceObject = GameObject as ResourceObject;
                                float Vdistance = Vector3.Distance(resourceObject.transform.position, character.transform.position);
                                if (Vdistance < 1000)
                                {
                                    string distance = String.Format("{0:0}", Vdistance);
                                    if (resourceObject.gameObject != this)
                                    {
                                        DrawLabel(resourceObject.transform.position, String.Format("{0} [{1}m]", resourceObject.name.Replace("(Clone)", ""), distance));
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        private void GiveScreen(int id)
        {
            CheckItemToGive();
            GUILayout.BeginVertical();
            if (GUILayout.Button("Go back", GUILayout.Width(100)))
            {
                SelectedPlayer = true;
                PlayerSelector = false;
                GiveItemMenu = false;
            }
            GUILayout.BeginHorizontal();
            Selected = GUILayout.Toolbar(Selected, toolbar);
            GUILayout.EndHorizontal();
            GUILayout.EndVertical();

            GUILayout.BeginHorizontal();
            GUILayout.Box("Amount to give: " + AmountToGive.ToString());
            AmountToGive = (int)Math.Round(GUILayout.HorizontalSlider(AmountToGive, 1, 250), 0);
            GUILayout.EndHorizontal();
            scrollposition0 = GUILayout.BeginScrollView(scrollposition0, GUILayout.Width((Screen.width - (Screen.width / 7)) - 100), GUILayout.Height(Screen.height - 190));
            switch (Selected)
            {
                case 0:
                    ItemToGive = GUILayout.SelectionGrid(ItemToGive, ItemTextures_Clothing, 5);
                    break;
                case 1:
                    ItemToGive = GUILayout.SelectionGrid(ItemToGive, ItemTextures_Medical, 5);
                    break;
                case 2:
                    ItemToGive = GUILayout.SelectionGrid(ItemToGive, ItemTextures_Weapons, 5);
                    break;
                case 3:
                    ItemToGive = GUILayout.SelectionGrid(ItemToGive, ItemTextures_Construction, 5);
                    break;
                case 4:
                    ItemToGive = GUILayout.SelectionGrid(ItemToGive, ItemTextures_Resource, 5);
                    break;
                case 5:
                    ItemToGive = GUILayout.SelectionGrid(ItemToGive, ItemTextures_Tools, 5);
                    break;
                case 6:
                    ItemToGive = GUILayout.SelectionGrid(ItemToGive, ItemTextures_Misc, 5);
                    break;
                default:
                    break;
            }
            GUILayout.EndScrollView();
        }

        private void PlayerMenu(int id)
        {
            if (NewDisplayName == null)
            {
                NewDisplayName = LookupName;
            }
            GUILayout.BeginVertical();
            if (GUILayout.Button("Go back"))
            {
                SelectedPlayer = false;
                PlayerSelector = true;
                LookupHWID = null;
                LookupName = null;
                NewDisplayName = null;
            }
            NewDisplayName = GUILayout.TextField(NewDisplayName);
            if (GUILayout.Button("Rename Player"))
            {
                //Rename - NewName - Target HWID
                AdminPlus.Instance.SendMessageToServer("Rename-" + ToBase64(NewDisplayName) + "-" + LookupHWID + "-");
                Rust.Notice.Popup("✔", "Renamed player!", 5);
            }

            if (GUILayout.Button("Give an item"))
            {
                SelectedPlayer = false;
                GiveItemMenu = true;
            }

            GUILayout.Box("Give a kit");
            //GiveKit - Kit - HWID
            GUILayout.BeginHorizontal();
            if (GUILayout.Button("Wood"))
            {
                AdminPlus.Instance.SendMessageToServer("GiveKit-KitWood-" + LookupHWID + "-");
            }
            if (GUILayout.Button("Metal"))
            {
                AdminPlus.Instance.SendMessageToServer("GiveKit-KitMetal-" + LookupHWID + "-");
            }
            GUILayout.EndHorizontal();
            GUILayout.BeginHorizontal();
            if (GUILayout.Button("Kevlar Suit"))
            {
                AdminPlus.Instance.SendMessageToServer("GiveKit-KitKevlar-" + LookupHWID + "-");
            }
            if (GUILayout.Button("Admin Suit"))
            {
                AdminPlus.Instance.SendMessageToServer("GiveKit-KitAdmin-" + LookupHWID + "-");
            }
            GUILayout.EndHorizontal();
            GUILayout.BeginHorizontal();
            if (GUILayout.Button("Weapons"))
            {
                AdminPlus.Instance.SendMessageToServer("GiveKit-KitWeapons-" + LookupHWID + "-");
            }
            if (GUILayout.Button("Uber kit"))
            {
                AdminPlus.Instance.SendMessageToServer("GiveKit-KitUber-" + LookupHWID + "-");
            }
            GUILayout.EndHorizontal();
            GUILayout.Box("Inventory Management");
            GUILayout.BeginHorizontal();
            if (GUILayout.Button("Clear Inventory"))
            {
                //ClearInventory - Target HWID
                AdminPlus.Instance.SendMessageToServer("ClearInventory-" + LookupHWID + "-");
            }
            if (GUILayout.Button("Clear Armour"))
            {
                //ClearInventory - Target HWID
                AdminPlus.Instance.SendMessageToServer("ClearArmour-" + LookupHWID + "-");
            }
            GUILayout.EndHorizontal();
            GUILayout.Box("Player Management");
            if (GUILayout.Button("Kick"))
            {
                //Kick - Target HWID
                if (LookupHWID != Hooks.HWID)
                {
                    AdminPlus.Instance.SendMessageToServer("Kick-" + LookupHWID + "-");
                }
                else
                {
                    Rust.Notice.Popup("✘", "You can not kick yourself!");
                }
            }
            if (GUILayout.Button("Ban"))
            {
                //Ban - Target HWID
                if (LookupHWID != Hooks.HWID)
                {
                    AdminPlus.Instance.SendMessageToServer("Ban-" + LookupHWID + "-");
                }
                else
                {
                    Rust.Notice.Popup("✘", "You can not ban yourself!");
                }
            }
            GUILayout.BeginHorizontal();
            if (GUILayout.Button("Mute"))
            {
                //Mute - Target HWID
                if (LookupHWID != Hooks.HWID)
                {
                    AdminPlus.Instance.SendMessageToServer("Mute-" + LookupHWID + "-");
                }
                else
                {
                    Rust.Notice.Popup("✘", "You can not mute yourself!");
                }
            }
            if (GUILayout.Button("UnMute"))
            {
                //UnMute - Target HWID
                AdminPlus.Instance.SendMessageToServer("UnMute-" + LookupHWID + "-");
            }
            GUILayout.EndHorizontal();
            GUILayout.BeginHorizontal();
            if (GUILayout.Button("Freeze"))
            {
                //Freeze - Target HWID
                AdminPlus.Instance.SendMessageToServer("Freeze-" + LookupHWID + "-");
            }
            if (GUILayout.Button("UnFreeze"))
            {
                //UnFreeze - Target HWID
                AdminPlus.Instance.SendMessageToServer("UnFreeze-" + LookupHWID + "-");
            }
            GUILayout.EndHorizontal();
            GUILayout.Box("Teleport options");
            if (GUILayout.Button("Bring to me"))
            {
                if (LookupHWID != Hooks.HWID)
                {
                    AdminPlus.Instance.SendMessageToServer("TeleportToMe-" + LookupHWID + "-");
                }
                else
                {
                    Rust.Notice.Popup("✘", "You can not teleport yourself to yourself!");
                }
            }
            if (GUILayout.Button("Go to Player"))
            {
                if (LookupHWID != Hooks.HWID)
                {
                    AdminPlus.Instance.SendMessageToServer("TeleportTo-" + LookupHWID + "-");
                }
                else
                {
                    Rust.Notice.Popup("✘", "You can not teleport to yourself!");
                }
            }
            if (GUILayout.Button("Silent Teleport"))
            {
                if (LookupHWID != Hooks.HWID)
                {
                    AdminPlus.Instance.SendMessageToServer("SilentTeleport-" + LookupHWID + "-");
                }
                else
                {
                    Rust.Notice.Popup("✘", "You can not teleport to yourself!");
                }
            }
            GUILayout.EndVertical();
        }

        private void PlayerEditorWindow(int id)
        {
            GUILayout.BeginVertical();
            Dictionary<string, string> dict = AdminPlus.Instance.GetPlayersList;
            if (dict.Keys.Count > 0)
            {
                scrollposition = GUILayout.BeginScrollView(scrollposition, GUILayout.Width((Screen.width / 2) - 30), GUILayout.Height(Screen.height - 130));
                foreach (string HWID in AdminPlus.Instance.GetPlayersList.Keys)
                {
                    if (GUILayout.Button(dict[HWID] + " = " + HWID))
                    {
                        LookupName = dict[HWID];
                        LookupHWID = HWID;
                        SelectedPlayer = true;
                        PlayerSelector = false;
                    }
                }
                GUILayout.EndScrollView();
            }
            else
            {
                GUILayout.Label("Looks like the server hasn't sent you any RPCs");
                GUILayout.Label("Not to worry, I'll add you to the list");
                if (GUILayout.Button(Hooks.PlayerName + " = " + Hooks.HWID))
                {
                    LookupName = Hooks.PlayerName;
                    LookupHWID = Hooks.HWID;
                    SelectedPlayer = true;
                    PlayerSelector = false;
                }
            }
            GUILayout.EndVertical();
        }

        private void NoClipMenu(int id)
        {
            GUILayout.BeginVertical();
            NoClip_Doors = GUILayout.Toggle(NoClip_Doors, "Doors");
            NoClip_Doorway = GUILayout.Toggle(NoClip_Doorway, "DoorWays");
            NoClip_Ceiling = GUILayout.Toggle(NoClip_Ceiling, "Ceilings");
            NoClip_Foundation = GUILayout.Toggle(NoClip_Foundation, "Foundations");
            NoClip_Wall = GUILayout.Toggle(NoClip_Wall, "Walls");
            NoClip_Pillar = GUILayout.Toggle(NoClip_Pillar, "Pillars");
            NoClip_Ramp = GUILayout.Toggle(NoClip_Ramp, "Ramps");
            NoClip_Stairs = GUILayout.Toggle(NoClip_Stairs, "Stairs");
            NoClip_WindowBars = GUILayout.Toggle(NoClip_WindowBars, "Window Bars");
            NoClip_Window = GUILayout.Toggle(NoClip_Window, "Windows");
            NoClip_WoodGate = GUILayout.Toggle(NoClip_WoodGate, "Wood Gate");
            NoClip_LargeSpike = GUILayout.Toggle(NoClip_LargeSpike, "Large Spike Wall");
            NoClip_SmallSpike = GUILayout.Toggle(NoClip_LargeSpike, "Small Spike Wall");
            NoClip_Barricade = GUILayout.Toggle(NoClip_Barricade, "Barricade");
            NoClip_Shelter = GUILayout.Toggle(NoClip_Shelter, "Shelters");
            GUILayout.EndVertical();
        }

        private void ESP(int id)
        {
            GUILayout.BeginVertical();
            ESPPlayers = GUILayout.Toggle(ESPPlayers, "Players");
            ESPAnimals = GUILayout.Toggle(ESPAnimals, "Animals");
            ESPLootables = GUILayout.Toggle(ESPLootables, "Lootables");
            ESPSleepers = GUILayout.Toggle(ESPSleepers, "Sleepers");
            ESPOres = GUILayout.Toggle(ESPOres, "Ores");
            ESPBases = GUILayout.Toggle(ESPBases, "Bases");
            GUILayout.EndVertical();
        }

        private void Menu(int id)
        {
            GUILayout.BeginVertical();
            if (GUILayout.Button("Toggle AdminMode"))
            {
                AdminPlus.Instance.SendMessageToServer("AdminMode-");
            }
            if (GUILayout.Button("Toggle Fly"))
            {
                Fly = !Fly;
                Rust.Notice.Inventory("", Fly ? "Enabled" : "Disabled");
            }
            if (GUILayout.Button("Toggle GodMode"))
            {
                AdminPlus.Instance.SendMessageToServer("GodMode-");
            }

            if (GUILayout.Button("Toggle AdminDoors"))
            {
                AdminDoors = !AdminDoors;
                NoClip_Doors = AdminDoors;
                Rust.Notice.Inventory("", AdminDoors ? "Enabled" : "Disabled");
            }
            if (GUILayout.Button("Toggle DestoryMode"))
            {
                AdminPlus.Instance.SendMessageToServer("AdminDestroy-");
            }
            if (GUILayout.Button("Learn all Blueprints"))
            {
                Rust.Notice.Popup("", LearnAllBPs() ? "You have learnt all BPs!" : "You already know all blueprints!", 10);
            }
            if (GUILayout.Button("NoClip Options"))
            {
                if (PlayerSelector)
                {
                    PlayerSelector = !PlayerSelector;
                }
                if (ESPoptions)
                {
                    ESPoptions = !ESPoptions;
                }
                if (SelectedPlayer)
                {
                    ResetPlayerSelector();
                    SelectedPlayer = !SelectedPlayer;
                }
                NoClip = !NoClip;
            }
            if (GUILayout.Button("ESP Options"))
            {
                if (PlayerSelector)
                {
                    PlayerSelector = !PlayerSelector;
                }
                if (NoClip)
                {
                    NoClip = !NoClip;
                }
                if (SelectedPlayer)
                {
                    ResetPlayerSelector();
                    SelectedPlayer = !SelectedPlayer;
                }
                ESPoptions = !ESPoptions;
            }
            if (GUILayout.Button("Lookup Player"))
            {
                if (ESPoptions)
                {
                    ESPoptions = !ESPoptions;
                }
                if (NoClip)
                {
                    NoClip = !NoClip;
                }
                if (SelectedPlayer)
                {
                    ResetPlayerSelector();
                    SelectedPlayer = !SelectedPlayer;
                }
                PlayerSelector = !PlayerSelector;
            }
            GUILayout.Label("Current Time: " + GetTime(EnvironmentControlCenter.Singleton.GetTime(), 0.1f));
            ServerTime = GUILayout.HorizontalSlider(ServerTime, 0f, 24f);
            if (GUILayout.Button("Change server time to: " + GetTime(ServerTime, 1f)))
            {
                AdminPlus.Instance.SendMessageToServer("ServerTime-" + ServerTime.ToString());
            }
            GUILayout.Label("Player Jump Height: " + GetTime(JumpHeight, 1f).ToString());
            JumpHeight = GUILayout.HorizontalSlider(JumpHeight, 0f, 20f);
            GUILayout.Label("Player Movement Speed: " + GetTime(SpeedLevel, 1f).ToString());
            SpeedLevel = GUILayout.HorizontalSlider(SpeedLevel, 0f, 20f);
            GUILayout.EndVertical();
        }

        private bool LearnAllBPs()
        {
            int count = 0;
            PlayerInventory playerInventory = Hooks.LocalPlayer.controllable.GetComponent<Character>().GetComponent<PlayerInventory>();

            if (playerInventory != null)
            {
                List<BlueprintDataBlock> boundBps = playerInventory.GetBoundBPs();
                foreach (BlueprintDataBlock blueprintDataBlock in Bundling.LoadAll<BlueprintDataBlock>())
                {
                    if (!boundBps.Contains(blueprintDataBlock))
                    {
                        boundBps.Add(blueprintDataBlock);
                        count++;
                    }
                }
            }
            if (count > 0)
            {
                return true;
            }
            return false;
        }

        public static string ToBase64(string text)
        {
            if (text == null)
            {
                return null;
            }

            try
            {
                byte[] textAsBytes = Encoding.UTF8.GetBytes(text);
                return Convert.ToBase64String(textAsBytes);
            }
            catch
            {
                return null;
            }
        }

        public static string Base64ToString(string encodedText)
        {
            if (encodedText == null)
            {
                return null;
            }

            try
            {
                byte[] textAsBytes = Convert.FromBase64String(encodedText);
                return Encoding.UTF8.GetString(textAsBytes);
            }
            catch
            {
                return null;
            }
        }

        private void DrawLabel(Vector3 point, string label)
        {
            DrawLabel(point, label, Color.white);
        }

        private void DrawLabel(Vector3 point, string label, Color color)
        {
            Vector3? vector = CameraFX.World2Screen(point);
            if (vector.HasValue)
            {
                Vector3 value = vector.Value;
                if (value.z > 0f)
                {
                    Vector2 vector2 = GUIUtility.ScreenToGUIPoint(value);
                    vector2.y = Screen.height - (vector2.y + 1f);
                    GUI.color = color != null ? color : Color.white;
                    GUI.Label(new Rect(vector2.x - 64f, vector2.y - 12f, 128f, 24f), label);
                }
            }
        }

        private void ResetPlayerSelector()
        {
            AdminPlus.Instance.PlayersList.Clear();
            LookupName = null;
            LookupHWID = null;
        }

        private void CheckItemToGive()
        {
            if (ItemToGive != -1)
            {
                GUIContent content;
                switch (Selected)
                {
                    case 0:
                        content = ItemTextures_Clothing[ItemToGive];
                        AdminPlus.Instance.SendMessageToServer("GiveItem-" + content.text + "-" + AmountToGive.ToString() + "-" + LookupHWID + "-");
                        ItemToGive = -1;
                        break;
                    case 1:
                        content = ItemTextures_Medical[ItemToGive];
                        AdminPlus.Instance.SendMessageToServer("GiveItem-" + content.text + "-" + AmountToGive.ToString() + "-" + LookupHWID + "-");
                        ItemToGive = -1;
                        break;
                    case 2:
                        content = ItemTextures_Weapons[ItemToGive];
                        AdminPlus.Instance.SendMessageToServer("GiveItem-" + content.text + "-" + AmountToGive.ToString() + "-" + LookupHWID + "-");
                        ItemToGive = -1;
                        break;
                    case 3:
                        content = ItemTextures_Construction[ItemToGive];
                        AdminPlus.Instance.SendMessageToServer("GiveItem-" + content.text + "-" + AmountToGive.ToString() + "-" + LookupHWID + "-");
                        ItemToGive = -1;
                        break;
                    case 4:
                        content = ItemTextures_Resource[ItemToGive];
                        AdminPlus.Instance.SendMessageToServer("GiveItem-" + content.text + "-" + AmountToGive.ToString() + "-" + LookupHWID + "-");
                        ItemToGive = -1;
                        break;
                    case 5:
                        content = ItemTextures_Tools[ItemToGive];
                        AdminPlus.Instance.SendMessageToServer("GiveItem-" + content.text + "-" + AmountToGive.ToString() + "-" + LookupHWID + "-");
                        ItemToGive = -1;
                        break;
                    case 6:
                        content = ItemTextures_Misc[ItemToGive];
                        AdminPlus.Instance.SendMessageToServer("GiveItem-" + content.text + "-" + AmountToGive.ToString() + "-" + LookupHWID + "-");
                        ItemToGive = -1;
                        break;
                    default:
                        ItemToGive = -1;
                        break;
                }
            }
        }

        public void NoClipSetter()
        {
            if (IsAlive)
            {
                foreach (StructureComponent structureComponent in Resources.FindObjectsOfTypeAll(typeof(StructureComponent)))
                {
                    switch (structureComponent.type)
                    {
                        case StructureComponent.StructureComponentType.Ceiling:
                            structureComponent.gameObject.SetActive(!NoClip_Ceiling);
                            break;
                        case StructureComponent.StructureComponentType.Doorway:
                            structureComponent.gameObject.SetActive(!NoClip_Doorway);
                            break;
                        case StructureComponent.StructureComponentType.Foundation:
                            structureComponent.gameObject.SetActive(!NoClip_Foundation);
                            break;
                        case StructureComponent.StructureComponentType.Pillar:
                            structureComponent.gameObject.SetActive(!NoClip_Pillar);
                            break;
                        case StructureComponent.StructureComponentType.Ramp:
                            structureComponent.gameObject.SetActive(!NoClip_Ramp);
                            break;
                        case StructureComponent.StructureComponentType.Stairs:
                            structureComponent.gameObject.SetActive(!NoClip_Stairs);
                            break;
                        case StructureComponent.StructureComponentType.Wall:
                            structureComponent.gameObject.SetActive(!NoClip_Wall);
                            break;
                        case StructureComponent.StructureComponentType.WindowWall:
                            structureComponent.gameObject.SetActive(!NoClip_Window);
                            break;
                    }
                }
                foreach (DeployableObject deployableObject in Resources.FindObjectsOfTypeAll(typeof(DeployableObject)))
                {
                    switch (deployableObject.name)
                    {
                        case "MetalDoor(Clone)":
                        case "WoodenDoor(Clone)":
                            deployableObject.gameObject.SetActive(!NoClip_Doors);
                            break; ;
                        case "MetalBarsWindow(Clone)":
                            deployableObject.gameObject.SetActive(!NoClip_WindowBars);
                            break;
                        case "WoodGate(Clone)":
                            deployableObject.gameObject.SetActive(!NoClip_WoodGate);
                            break;
                        case "Barricade_Fence_Deployable(Clone)":
                            deployableObject.gameObject.SetActive(!NoClip_Barricade);
                            break;
                        case "LargeWoodSpikeWall(Clone)":
                            deployableObject.gameObject.SetActive(!NoClip_LargeSpike);
                            break;
                        case "Wood_Shelter(Clone)":
                            deployableObject.gameObject.SetActive(!NoClip_Shelter);
                            break;
                            //Small Spikes
                            //WoodGateway(Clone), Not needed?
                    }
                }
            }
        }

        public string GetTime(float time, float rounding)
        {
            return time.RoundToNearest(rounding).ToString();
        }
    }
}
