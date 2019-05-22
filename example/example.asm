
set v0, 5
start:
	sub v0, 1
	eql v1, v0
	jmc exit
	jmp start

exit:
