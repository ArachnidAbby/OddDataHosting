# Encryption Methods

- Usernames are encrypted with `SHA256`. 
- Using a multi Fernet. The server stores 3 keys, one being the password. The remote stores two keys, then enters there password to generate the third key. (used to encrypt the "Message" portion of the packet)


# Server Outbound
*(size: 1024 Bytes)*
```json
{
    "Status":"SUCCESS OR ERROR CODE",
    "Message": "Encrypted Message"
}
```

## Status Codes

- Success
- Wrong Version
- Invalid Command
- Script Not Found
- File Not Found
- Content On Next Packet
- Incorrect Credentials

## Large Packets
The first packet's message will be set as an empty string and the status code ``Content On Next Packet`` will be sent. This tells the client to await for however many packets are specified in the "Packs" section of the first message. The packet size for those secondary packets will be 64KB (65536 Bytes)



# Server inbound

## Commands

- `Close`
- `Info`
- `Create <File Name> [Encrypted <key>]`
- `Get  <File Name> [Encrypted <key>]`
- `Run <Registered name> <Func> [args]`
- `SqliteRun <request>` (Not Implemented Yet)

## Standard Packet (Server InBound)
*(size: 1024 Bytes)*
```json
{
    "Message": {
        "Command": "Command",
        "Args" : [
            "Arg1"
        ]
    }
}

```

## Establish Connection Packet (Server InBound)
*(size: 1024 Bytes)*
```json
{
    "user": "SHA265 Username",
    "version": 1,
    "Message":"encrypted -> Test"
}
```