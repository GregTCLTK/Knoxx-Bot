async def execute(server, client):
    await client.send_message(server.owner, "```Hey vielen Dank das ich nun auf deinem Discord sein kann! Ich habe schon mal insgesamt 7 Rollen erstellt die genutzt werden das zum Beispiel nicht einfach ein normaler User dern Chat leeren kann deswegen empfehle ich dir diese Rollen so bei zu behalten wie sind jetzt gerade sind!```")
    Owner=await client.create_role(server)
    role_name = "Owner"
    await client.edit_role(server, Owner, name=role_name)
    Administrator=await client.create_role(server)
    role_name = "Administrator"
    await client.edit_role(server, Administrator, name=role_name)
    Bots=await client.create_role(server)
    role_name = "Bots"
    await client.edit_role(server, Bots, name=role_name)
    Moderator=await client.create_role(server)
    role_name = "Moderator"
    await client.edit_role(server, Moderator, name=role_name) 
    Supporter=await client.create_role(server)
    role_name = "Supporter"
    await client.edit_role(server, Supporter, name=role_name)   
    VIP=await client.create_role(server)
    role_name = "VIP"
    await client.edit_role(server, VIP, name=role_name)
    Member=await client.create_role(server)
    role_name = "Member"
    await client.edit_role(server, Member, name=role_name)
    print("OMG 1 neuer Server mit dem Namen: %s" % (server.name))