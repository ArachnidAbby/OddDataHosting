read -p "Enter Username: "  user
read -s -p "Enter Password: "  pass
echo ""
python3 Main.py NewUser $user $pass