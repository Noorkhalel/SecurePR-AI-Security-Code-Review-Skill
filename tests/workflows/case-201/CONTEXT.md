# Synthetic evaluation contract

Inert source-review fixture; do not execute.

A verified server-derived actor with tenant membership can invoke invite. Managers may invite only members; administrators may invite members or managers. No caller may assign administrator through this operation. The role hierarchy is explicit in policy.js. The server-owned invitations list is later consumed exactly as recorded, granting its role in its tenant. No other role filter exists. Identifier/email syntax and duplicate handling are outside this focused policy test.
