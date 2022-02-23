def update_users(a,b,c,d):
    new = str(a)+","+ str(b)+","+ str(c)+","+ str(d)
    with open("data/users.txt", "r", encoding="utf-8") as users:
        users = [line.rstrip() for line in users]
    if new not in users:
        users.append(new)
    file = open("data/users.txt", "w", encoding="utf-8")
    for user in users:
        file.write(user)
        file.write("\n")
    file.close()
    #print("Обновление списка пользователей завершено")
