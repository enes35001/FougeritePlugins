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
        //Menu settings
        private GUIStyle guiStyle = new GUIStyle();
        internal int Selected = 0;
        internal Vector2 scrollposition;
        internal Vector2 scrollposition0;
        //private bool AlwaysAtWorkbench = false;

        internal bool Fly = false;

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
                    if (GUI.Button(new Rect(5, 5, 80, 20), "FLY"))
                    {
                        AdminPlus.Enabled = !AdminPlus.Enabled;
                        if (!ChatUI.IsVisible() && !ConsoleWindow.IsVisible() && !MainMenu.IsVisible())
                        {
                            Screen.lockCursor = !AdminPlus.Enabled;
                        }
                    }                      
                }
            }
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

        private void Menu(int id)
        {
            GUILayout.BeginVertical();
            if (GUILayout.Button("Toggle Fly"))
            {
                Fly = !Fly;
                Rust.Notice.Inventory("", Fly ? "Enabled" : "Disabled");
            }

        private void ResetPlayerSelector()
        {
            AdminPlus.Instance.PlayersList.Clear();
            LookupName = null;
            LookupHWID = null;
        }


        public string GetTime(float time, float rounding)
        {
            return time.RoundToNearest(rounding).ToString();
        }
    }
}
