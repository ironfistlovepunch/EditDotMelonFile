import appex
import melon編集

print(appex.is_running_extension())
print(appex.get_text())

file_path = appex.get_file_path()
print(file_path)
melon編集.main(file_path)
