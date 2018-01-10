pragma solidity ^0.4.0;

contract OrgData {

    /*struct Organisation {
        address id;
        string name; // string until model is defined
        bool active; // potentially change to enum
        bytes4[] asnList;
        bytes4[] prefixesV4;
        bytes16[] prefixesV6;
    }*/

    /*struct RouteV4 {
        string desc;
        bool active;
        bytes4 route;
    }*/

    /*mapping (address => string) public orgs;*/

    string public prefixes;

    function OrgData() {
        prefixes = '10.10.1.0/24';
    }

    function set(string set_prefixes) {
        prefixes = set_prefixes;
    }

    function get() constant returns (string) {
        return prefixes;
    }
}
