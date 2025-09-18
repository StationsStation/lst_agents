# User Interaction Protocol

## Description

...

## Specification

```yaml
name: user_interaction
author: eightballer
version: 0.1.0
description: A protocol for handling interactive user-agent communications within applications, facilitating notifications, commands, confirmations, and error handling.
license: Apache-2.0
aea_version: '>=1.0.0, <2.0.0'
protocol_specification_id: eightballer/user_interaction:0.1.0
speech_acts:
  notification:
    body: pt:str
    title: pt:optional[pt:str]
    attach: pt:optional[pt:str]
  user_command:
    command: pt:str
    data: pt:optional[pt:dict[pt:str, pt:bytes]]
  request_confirmation:
    message: pt:str
  user_confirmation:
    confirmed: pt:bool
  error:
    error_code: ct:ErrorCode
    error_msg: pt:str
    error_data: pt:optional[pt:dict[pt:str, pt:bytes]]
  end: {}
---
ct:ErrorCode: |
  enum ErrorCodeEnum {
      UNKNOWN_ERROR = 0;
      COMMAND_NOT_SUPPORTED = 1;
      COMMAND_FAILED = 2;
      NOTIFICATION_FAILED = 3;
      INVALID_DATA = 4;
    }
  ErrorCodeEnum error_code = 1;
---
initiation: [notification, user_command]
reply:
  notification: [user_command, request_confirmation, error, end]
  user_command: [notification, request_confirmation, error]
  request_confirmation: [user_confirmation, error]
  user_confirmation: [end, error]
  error: []
  end: []
roles: {user, agent}
end_states: [end, error]
termination: [end, error]
keep_terminal_state_dialogues: true
```