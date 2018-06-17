using UnityEngine;

namespace StackSizesClient
{
    public class StackSizesRPC : MonoBehaviour
    {
        public void Start()
        {
            StackSizesClient.Instance.SendMessageToServer("UpdateStackSizes-");
        }

        [RPC]
        public void StackSizes(int uniqueid, int stacksize)
        {
            DatablockDictionary.GetByUniqueID(uniqueid)._maxUses = stacksize;
        }
    }
}
