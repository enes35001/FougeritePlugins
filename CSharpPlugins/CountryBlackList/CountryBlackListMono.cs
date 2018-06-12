using System;
using System.ComponentModel;
using System.IO;
using System.Linq;
using Fougerite;
using UnityEngine;

namespace CountryBlackList
{
    public class CountryBlackListMono : MonoBehaviour
    {
        public void HandleGeoIPRequest(Fougerite.Player player)
        {
            BackgroundWorker BGW = new BackgroundWorker();
            BGW.DoWork += new DoWorkEventHandler(HandlePlayerConnection);
            BGW.RunWorkerAsync(player);
        }

        private void HandlePlayerConnection(object sender, DoWorkEventArgs doWorkEventArgs)
        {
            Fougerite.Player player = (Fougerite.Player)doWorkEventArgs.Argument;
            var data = GeoIP.GeoIP.Instance.GetDataOfIP(player.IP);
            if (data == null)
            {
                if (CountryBlackList.Instance.Show_Accept_Message)
                {
                    string message = CountryBlackList.Instance.Join_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", CountryBlackList.Instance.Unknown_Location);
                    Server.GetServer().BroadcastFrom("CountryBlackList", message);
                }
                if (CountryBlackList.Instance.Log_TimedOut_Connections)
                {
                    CountryBlackList.Instance.file = new System.IO.StreamWriter(Path.Combine(CountryBlackList.Instance.ModuleFolder, "TimedOut Connections.log"), true);
                    CountryBlackList.Instance.file.WriteLine(DateTime.Now + ": " + player.SteamID + "=" + player.Name + " [" + player.IP + "]");
                    CountryBlackList.Instance.file.Close();
                }
                return;
            }
            string countrycode = data.CountryShort;
            if (CountryBlackList.Instance.BlackList.Any(countrycode.Contains))
            {
                if (CountryBlackList.Instance.Use_WhiteList)
                {
                    if (CountryBlackList.Instance.OnWhiteList(player.SteamID, player.IP))
                    {
                        if (CountryBlackList.Instance.Show_Accept_Message)
                        {
                            string message = CountryBlackList.Instance.Join_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", data.Country);
                            Server.GetServer().BroadcastFrom("CountryBlackList", message);
                        }
                        return;
                    }
                }
                if (CountryBlackList.Instance.Show_Denied_Message)
                {
                    string message = CountryBlackList.Instance.Server_Disconnect_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", data.Country);
                    Server.GetServer().BroadcastFrom("CountryBlackList", message);
                }
                player.MessageFrom("CountryBlackList", CountryBlackList.Instance.Player_Disconnect_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", data.Country));
                player.Disconnect();
            }
            else
            {
                if (CountryBlackList.Instance.Show_Accept_Message)
                {
                    string message = CountryBlackList.Instance.Join_Message.Replace("%PLAYER%", player.Name).Replace("%COUNTRY%", data.Country);
                    Server.GetServer().BroadcastFrom("CountryBlackList", message);
                }
            }
        }
    }
}
