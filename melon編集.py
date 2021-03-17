import sys
import os
import io
import struct
import re

import xml.etree.ElementTree as ET
from unicodedata import normalize

def main(sourcefile):
	#入力ファイル
	filename = os.path.basename(sourcefile)
	filedir = os.path.dirname(sourcefile)
	file_size = os.path.getsize(sourcefile)
	
	print(sourcefile)
	print(filename)
	print(filedir)
	print(file_size)

	#元のファイルを開く
	with open(sourcefile, mode='rb') as fi:
		#RIFF
		id = fi.read(4)
		print(id)
		#ファイルサイズ	
		file_size_b = fi.read(4)
		print(file_size_b)
		file_size = int(struct.unpack("<i",file_size_b)[0]) #リトルエンディアン
		print("file_size:%d" % file_size)
		
		#フォームタイプ
		id = fi.read(4)
		print(id)
	
		#META
		id = fi.read(4)
		print(id)
	
		#METAデータサイズ
		meta_size_b = fi.read(4)
		meta_size = int(struct.unpack("<i",meta_size_b)[0]) #リトルエンディアン
		print(meta_size_b)
		print("meta_size:%d" % meta_size)
	
		#METAデータ
		meta = fi.read(meta_size)
		print(meta)
	
		#file_type
		root = ET.fromstring(meta)
		file_type = root.find("file_type").text
		print(file_type)
		title = root.find("title").text
		print(title)
	
		#ファイルサイズ計算
		file_size_new = file_size - len(file_type) + 3
		file_size_new_b = struct.pack("<i",file_size_new)
		print("file_size_new:%d" % file_size_new)
		print(file_size_new_b)
	
		#metaサイズ計算
		meta_size_new = meta_size - len(file_type) + 3
		meta_size_new_b = struct.pack("<i",meta_size_new)
		print("meta_size_new:%d" % meta_size_new)
		print(meta_size_new_b)
	
	#出力ファイル名
	if file_type == "zip":
		outfile = normalize("NFC",sourcefile.replace(".melon",".zip.cbz.melon"))
	else:
		outfile = normalize("NFC",sourcefile.replace(".melon","."+file_type+".melon"))
	
	#変換用ファイル作成
	with open(outfile,mode="wb") as fo: #出力
		with open(sourcefile,mode="rb") as fi: #入力
			#RIFF
			id = fi.read(4)
			print(id)
			fo.write(id)
			
			#ファイルサイズ(一応変更する)
			fo.write(file_size_new_b)
			fi.seek(4,1) #サイズを読み飛ばす
			
			#フォームタイプ+META
			fo.write(fi.read(8))
	
			#METAサイズ
			fo.write(meta_size_new_b)
			fi.seek(4,1) #サイズを読み飛ばす
			
			#METAデータ部
			meta = fi.read(meta_size)
			print(meta)
			meta_new = re.sub(b"(?<=\<file_type\>)[^\<]+(?=\</file_type\>)",b"pdf",meta)
			print(meta_new)
			fo.write(meta_new)
			
			#パディング
			if meta_size_new % 2 != 0:
				#新データが奇数なので0を追加
				print("0追加")
				fo.write(b"0")
	
			#0パディング対策
			if meta_size % 2 != 0:
				#元データが奇数なので0を読み飛ばす
				print("0削除")
				fi.seek(1,1)
	
			#残りの部分
			fo.write(fi.read())
	
	#出力ファイル名を表示して終了
	print(outfile)

#プログラム実行
if __name__ == "__main__":
	#ファイル入力
	if len(sys.argv) == 1:
		sourcefile = "test.melon"

	else:
		sourcefile = sys.argv[-1]

	main(sourcefile)
