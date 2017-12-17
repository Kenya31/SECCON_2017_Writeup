# -*- coding:utf-8 -*-

import cv2
import numpy as np
import sys
import copy
import kociemba
import zbar

args = sys.argv
src_dir = './src_img/'
wrk_dir = './wrk_img/'
baseColors = {}

def prepareView(imgs, target):
    result = copy.copy(imgs)

    if (target == 'U'):
        # turn left 90 degree
        result['R'] = turnLeft90(imgs['R'])
        # turn right 90 degree
        result['L'] = turnRight90(imgs['L'])
        # turn 180 degree
        result['U'] = turn180(imgs['U'])

    elif (target == 'R'):
        # turn right 90 degree
        result['U'] = turnRight90(imgs['U'])
        # turn left 90 degree
        result['D'] = turnLeft90(imgs['D'])

    elif (target == 'F'):
        pass

    elif (target == 'D'):
        # turn right 90 degree
        result['R'] = turnRight90(imgs['R'])
        # turn left 90 degree
        result['L'] = turnLeft90(imgs['L'])
        # turn 180 degree
        result['D'] = turn180(imgs['D'])

    elif (target == 'L'):
        # turn left 90 degree
        result['U'] = turnLeft90(imgs['U'])
        # turn right 90 degree
        result['D'] = turnRight90(imgs['D'])

    elif (target == 'B'):
        # turn 180 degree
        result['U'] = turn180(imgs['U'])
        # turn 180 degree
        result['D'] = turn180(imgs['D'])


    return result


def revertView(imgs, target):
    result = copy.copy(imgs)

    if (target == 'U'):
        # turn right 90 degree
        result['R'] = turnRight90(imgs['R'])
        # turn left 90 degree
        result['L'] = turnLeft90(imgs['L'])
        # turn 180 degree
        result['U'] = turn180(imgs['U'])
        
    elif (target == 'R'):
        # turn right 90 degree
        result['U'] = turnLeft90(imgs['U'])
        # turn left 90 degree
        result['D'] = turnRight90(imgs['D'])

    elif (target == 'F'):
        pass

    elif (target == 'D'):
        # turn right 90 degree
        result['R'] = turnLeft90(imgs['R'])
        # turn left 90 degree
        result['L'] = turnRight90(imgs['L'])
        # turn 180 degree
        result['D'] = turn180(imgs['D'])

    elif (target == 'L'):
        # turn left 90 degree
        result['U'] = turnRight90(imgs['U'])
        # turn right 90 degree
        result['D'] = turnLeft90(imgs['D'])

    elif (target == 'B'):
        # turn 180 degree
        result['U'] = turn180(imgs['U'])
        # turn 180 degree
        result['D'] = turn180(imgs['D'])


    return result


def saveImageFiles(caseName, angle, imgs):
    suffixes = ['U', 'R', 'F', 'D', 'L', 'B']

    for suffix in imgs.keys():
        dstFilePath = '%s%s_%03d_%s.png' % (wrk_dir, caseName, angle, suffix)
        cv2.imwrite(dstFilePath, imgs[suffix])
    

def loadImageFiles(caseName):
    suffixes = ['U', 'R', 'F', 'D', 'L', 'B']
    result = {}

    for suffix in suffixes:
        srcFilePath = '%s%s_%s.png' % (wrk_dir, caseName, suffix)
        result[suffix] = cv2.imread(srcFilePath)
        #print "[DEBUG] result[%s]: %s" % (suffix, srcFilePath)

    return result
    

def rotate180(caseName, target):
    rotateRight90(caseName, target)
    rotateRight90(caseName, target)


def rotateLeft90(caseName, target):
    rotateRight90(caseName, target)
    rotateRight90(caseName, target)
    rotateRight90(caseName, target)


def rotateRight90(caseName, target):
    tmp_wrk_dir = wrk_dir + caseName

    src_imgs = loadImageFiles(caseName)
    tmp_imgs = copy.copy(src_imgs)
    if (target == 'U'):
        tmp_imgs['U'] = copy.copy(src_imgs['B'])
        tmp_imgs['R'] = copy.copy(src_imgs['R'])
        tmp_imgs['F'] = copy.copy(src_imgs['U'])
        tmp_imgs['D'] = copy.copy(src_imgs['F'])
        tmp_imgs['L'] = copy.copy(src_imgs['L'])
        file_name_u = tmp_wrk_dir + '_B.png'
        file_name_r = tmp_wrk_dir + '_R.png'
        file_name_f = tmp_wrk_dir + '_U.png'
        file_name_d = tmp_wrk_dir + '_F.png'
        file_name_l = tmp_wrk_dir + '_L.png'

    elif (target == 'R'):
        tmp_imgs['U'] = copy.copy(src_imgs['U'])
        tmp_imgs['R'] = copy.copy(src_imgs['B'])
        tmp_imgs['F'] = copy.copy(src_imgs['R'])
        tmp_imgs['D'] = copy.copy(src_imgs['D'])
        tmp_imgs['L'] = copy.copy(src_imgs['F'])
        file_name_u = tmp_wrk_dir + '_U.png'
        file_name_r = tmp_wrk_dir + '_B.png'
        file_name_f = tmp_wrk_dir + '_R.png'
        file_name_d = tmp_wrk_dir + '_D.png'
        file_name_l = tmp_wrk_dir + '_F.png'

    elif (target == 'F'):
        tmp_imgs['U'] = copy.copy(src_imgs['U'])
        tmp_imgs['R'] = copy.copy(src_imgs['R'])
        tmp_imgs['F'] = copy.copy(src_imgs['F'])
        tmp_imgs['D'] = copy.copy(src_imgs['D'])
        tmp_imgs['L'] = copy.copy(src_imgs['L'])
        file_name_u = tmp_wrk_dir + '_U.png'
        file_name_r = tmp_wrk_dir + '_R.png'
        file_name_f = tmp_wrk_dir + '_F.png'
        file_name_d = tmp_wrk_dir + '_D.png'
        file_name_l = tmp_wrk_dir + '_L.png'

    elif (target == 'D'):
        tmp_imgs['U'] = copy.copy(src_imgs['F'])
        tmp_imgs['R'] = copy.copy(src_imgs['R'])
        tmp_imgs['F'] = copy.copy(src_imgs['D'])
        tmp_imgs['D'] = copy.copy(src_imgs['B'])
        tmp_imgs['L'] = copy.copy(src_imgs['L'])
        file_name_u = tmp_wrk_dir + '_F.png'
        file_name_r = tmp_wrk_dir + '_R.png'
        file_name_f = tmp_wrk_dir + '_D.png'
        file_name_d = tmp_wrk_dir + '_B.png'
        file_name_l = tmp_wrk_dir + '_L.png'

    elif (target == 'L'):
        tmp_imgs['U'] = copy.copy(src_imgs['U'])
        tmp_imgs['R'] = copy.copy(src_imgs['F'])
        tmp_imgs['F'] = copy.copy(src_imgs['L'])
        tmp_imgs['D'] = copy.copy(src_imgs['D'])
        tmp_imgs['L'] = copy.copy(src_imgs['B'])
        file_name_u = tmp_wrk_dir + '_U.png'
        file_name_r = tmp_wrk_dir + '_F.png'
        file_name_f = tmp_wrk_dir + '_L.png'
        file_name_d = tmp_wrk_dir + '_D.png'
        file_name_l = tmp_wrk_dir + '_B.png'

    elif (target == 'B'):
        tmp_imgs['U'] = copy.copy(src_imgs['U'])
        tmp_imgs['R'] = copy.copy(src_imgs['L'])
        tmp_imgs['F'] = copy.copy(src_imgs['B'])
        tmp_imgs['D'] = copy.copy(src_imgs['D'])
        tmp_imgs['L'] = copy.copy(src_imgs['R'])
        file_name_u = tmp_wrk_dir + '_U.png'
        file_name_r = tmp_wrk_dir + '_L.png'
        file_name_f = tmp_wrk_dir + '_B.png'
        file_name_d = tmp_wrk_dir + '_D.png'
        file_name_l = tmp_wrk_dir + '_R.png'

    #
    wrk_imgs = prepareView(tmp_imgs, target)
    dst_imgs = {}

    # F 90 degree
    dst_imgs['F'] = turnRight90(wrk_imgs['F'])

    # (L3, L6, L9) + [U1, U2, U3, U4, U5, U6)
    wrk_img = turnRight90(wrk_imgs['L'])
    add_img = trimTarget(wrk_img, 'D')       
    dst_imgs['U'] = overWrite(wrk_imgs['U'], add_img, 'D')

    # (U7, U8, U9) + (R2, R3, R5, R6, R8, R9) 
    wrk_img = turnRight90(wrk_imgs['U'])
    add_img = trimTarget(wrk_img, 'L')       
    dst_imgs['R'] = overWrite(wrk_imgs['R'], add_img, 'L')

    # (R1, R4, R7) + (D4, D5, D6, D7, D8, D9) 
    wrk_img = turnRight90(wrk_imgs['R'])
    add_img = trimTarget(wrk_img, 'U')       
    dst_imgs['D'] = overWrite(wrk_imgs['D'], add_img, 'U')

    # (D1, D2, D3) + (L1, L2, L4, L5, L7, L8) 
    wrk_img = turnRight90(wrk_imgs['D'])
    add_img = trimTarget(wrk_img, 'R')       
    dst_imgs['L'] = overWrite(wrk_imgs['L'], add_img, 'R')

    #
    dst_imgs['B'] = wrk_imgs['B']
    result = revertView(dst_imgs, target)

    cv2.imwrite(file_name_u, result['U'])
    cv2.imwrite(file_name_r, result['R'])
    cv2.imwrite(file_name_f, result['F'])
    cv2.imwrite(file_name_d, result['D'])
    cv2.imwrite(file_name_l, result['L'])
        

def turn180(src):
    result = np.zeros([246, 246, 3], np.uint8)

    start_x = 0
    end_x = 246
    start_y = 0
    end_y = 246

    dst_start_x = 245
    dst_x = dst_start_x
    dst_start_y = 245
    dst_y = dst_start_y
    for src_x in range(start_x, end_x, 1):
        dst_y = dst_start_y
        for src_y in range(start_y, end_y):
            # [245, 245] <= [0, 0]
            # [245, 244] <= [0, 1]
#            print "dst[%d, %d] <= src[%d, %d]" % (dst_x, dst_y, src_x, src_y)
            result[dst_x, dst_y] = src[src_x, src_y]
            dst_y -= 1
        dst_x -= 1

    return result


def turnRight90(src):
    result = np.zeros([246, 246, 3], np.uint8)

    start_x = 0
    end_x = 246
    start_y = 0
    end_y = 246

    dst_start_x = 0
    dst_x = dst_start_x
    dst_start_y = 245
    dst_y = dst_start_y
    for src_x in range(start_x, end_x, 1):
        dst_x = dst_start_x
        for src_y in range(start_y, end_y):
            # [0, 245] <= [0, 0]
            # [1, 245] <= [0, 1]
#            print "dst[%d, %d] <= src[%d, %d]" % (dst_x, dst_y, src_x, src_y)
            result[dst_x, dst_y] = src[src_x, src_y]
            dst_x += 1
        dst_y -= 1

    return result


def turnLeft90(src):
    result = np.zeros([246, 246, 3], np.uint8)

    start_x = 0
    end_x = 246
    start_y = 0
    end_y = 246

    dst_start_x = 245
    dst_x = dst_start_x
    dst_start_y = 0
    dst_y = 0
    for src_x in range(start_x, end_x, 1):
        dst_x = dst_start_x
        for src_y in range(start_y, end_y):
            # [245, 0] <= [0, 0]
            result[dst_x, dst_y] = src[src_x, src_y]
#            print "dst[%d, %d] <= src[%d, %d]" % (dst_x, dst_y, src_x, src_y)
            dst_x -= 1
        dst_y += 1

    return result


def _overWrite(src, add_img, start_x, end_x, start_y, end_y):
    result = copy.copy(src)

    dst_y = start_y
    for src_y in range(start_y, end_y, 1):
        dst_x = start_x
        for src_x in range(start_x, end_x):
            result[dst_x, dst_y] = add_img[src_x, src_y]
            dst_x += 1
        dst_y += 1

    return result


def overWrite(src, add_img, target):

    if (target == 'U'):
        # Upper row
        result = _overWrite(src, add_img, 0, 82, 0, 82 * 3)

    elif (target == 'D'):
        # Right column
        result = _overWrite(src, add_img, 82 * 2, 82 * 3, 0, 82 * 3)

    elif (target == 'R'):
        # Right column
        result = _overWrite(src, add_img, 0, 82 * 3, 82 * 2, 82 * 3)

    elif (target == 'L'):
        # Left column
        result = _overWrite(src, add_img, 0, 82 * 3, 0, 82)

    elif (target == 'C'):
        # Center
        result = _overWrite(src, add_img, 82, 82 * 2, 82, 82 * 2)

    return result


def _trimTarget(src, start_x, end_x, start_y, end_y):
    result = np.zeros([246, 246, 3], np.uint8)

    dst_y = start_y
    for src_y in range(start_y, end_y, 1):
        dst_x = start_x
        for src_x in range(start_x, end_x):
#            print "[src_x, src_y]%s %s" % (src_x, src_y)
            result[dst_x, dst_y] = src[src_x, src_y]
            dst_x += 1
        dst_y += 1

    return result


def trimTarget(src, target):

    if (target == 'U'):
        # Upper row
        result = _trimTarget(src, 0, 82, 0, 82 * 3)

    elif (target == 'D'):
        # Right column
        result = _trimTarget(src, 82 * 2, 82 * 3, 0, 82 * 3)

    elif (target == 'R'):
        # Right column
        result = _trimTarget(src, 0, 82 * 3, 82 * 2, 82 * 3)

    elif (target == 'L'):
        # Left column
        result = _trimTarget(src, 0, 82 * 3, 0, 82)

    elif (target == 'C'):
        # Center
        result = _trimTarget(src, 82, 82 * 2, 82, 82 * 2)

    return result


def checkCenterColor(src):
    src_start_x = 82
    src_end_x = src_start_x + 82
    src_start_y = 82
    src_end_y = src_start_y + 82

    dst_y = src_start_y
    for src_y in range(src_start_y, src_end_y, 1):
        dst_x = src_start_x
        for src_x in range(src_start_x, src_end_x):
#            print "[src_x, src_y]%s %s" % (src_x, src_y)
            b, g, r = src[src_x, src_y]
            result = (b, g, r)
            if (result != (0, 0, 0)):
                break
            dst_x += 1
        dst_y += 1
    
    return result


def checkBaseColor(imgs):
    sequence = ['U', 'R', 'F', 'D', 'L', 'B']

    for seq in sequence:
        baseColors[seq] = checkCenterColor(imgs[seq])
    

# {
#  'B': (96, 158, 0),
#  'D': (255, 255, 255),
#  'F': (186, 81, 0),
#  'L': (58, 30, 196),
#  'R': (0, 88, 255),
#  'U': (0, 213, 255)
# }
def checkColor(b, g, r):
    result = ''

    for key in baseColors.keys():
        if baseColors[key] == (b, g, r):
            result = key
            break

    return result


# Posision
# 1 2 3
# 4 5 6
# 7 8 9
def checkPosition(src, pos):
    width = 246
    height = 246
    result = ''

    if (pos == 1):
        src_start_x = 0
        src_end_x = src_start_x + 82
        src_start_y = 0
        src_end_y = src_start_y + 82
    elif (pos == 2):
        src_start_x = 0
        src_end_x = src_start_x + 82
        src_start_y = 82
        src_end_y = src_start_y + 82
    elif (pos == 3):
        src_start_x = 0
        src_end_x = src_start_x + 82
        src_start_y = 82 * 2
        src_end_y = src_start_y + 82
    elif (pos == 4):
        src_start_x = 82
        src_end_x = src_start_x + 82
        src_start_y = 0
        src_end_y = src_start_y + 82
    elif (pos == 5):
        src_start_x = 82
        src_end_x = src_start_x + 82
        src_start_y = 82
        src_end_y = src_start_y + 82
    elif (pos == 6):
        src_start_x = 82
        src_end_x = src_start_x + 82
        src_start_y = 82 * 2
        src_end_y = src_start_y + 82
    elif (pos == 7):
        src_start_x = 82 * 2
        src_end_x = src_start_x + 82
        src_start_y = 0
        src_end_y = src_start_y + 82
    elif (pos == 8):
        src_start_x = 82 * 2
        src_end_x = src_start_x + 82
        src_start_y = 82
        src_end_y = src_start_y + 82
    elif (pos == 9):
        src_start_x = 82 * 2
        src_end_x = src_start_x + 82
        src_start_y = 82 * 2
        src_end_y = src_start_y + 82

    dst_y = src_start_y
    for src_y in range(src_start_y, src_end_y, 1):
        dst_x = src_start_x
        for src_x in range(src_start_x, src_end_x):
            b, g, r = src[src_x, src_y]
#            print "[src_x, src_y]%s %s color[%d, %d, %d]" % (src_x, src_y, b, g, r)
            if (b, g, r) == (0, 0, 0):
                pass
            else:
                result = checkColor(b, g, r)
                break
            dst_x += 1
        dst_y += 1

    return result


def checkImage(src):
    result = ""

    for i in range(1, 10):
        result += checkPosition(src, i)
    
    return result


def rotateCenter(src):
    result = copy.copy(src)

    add_img = trimTarget(result, 'C')
    add_img = turnRight90(add_img)
    result = overWrite(result, add_img, 'C')
    
    return result


def rotateCenterAll(imgs):
    sequence = ['U', 'R', 'F', 'D', 'L', 'B']
    result = copy.copy(imgs)

    for key in sequence:
        result[key] = rotateCenter(result[key])
    
    return result


def serialize(imgs):
    sequence = ['U', 'R', 'F', 'D', 'L', 'B']
    result = ""

    for key in sequence:
        result += checkImage(imgs[key])

    return result


def solve(caseName, solveSeq):

    l = solveSeq.split(' ')

    for target in l:
        print "rotate[%s]" % target
        
        if (target == "U"):
            rotateRight90(caseName, 'U')
        elif (target == "U2"):
            rotate180(caseName, 'U')
        elif (target == "U'"):
            rotateLeft90(caseName, 'U')
        elif (target == "R"):
            rotateRight90(caseName, 'R')
        elif (target == "R2"):
            rotate180(caseName, 'R')
        elif (target == "R'"):
            rotateLeft90(caseName, 'R')
        elif (target == "F"):
            rotateRight90(caseName, 'F')
        elif (target == "F2"):
            rotate180(caseName, 'F')
        elif (target == "F'"):
            rotateLeft90(caseName, 'F')
        elif (target == "D"):
            rotateRight90(caseName, 'D')
        elif (target == "D2"):
            rotate180(caseName, 'D')
        elif (target == "D'"):
            rotateLeft90(caseName, 'D')
        elif (target == "L"):
            rotateRight90(caseName, 'L')
        elif (target == "L2"):
            rotate180(caseName, 'L')
        elif (target == "L'"):
            rotateLeft90(caseName, 'L')
        elif (target == "B"):
            rotateRight90(caseName, 'B')
        elif (target == "B2"):
            rotate180(caseName, 'B')
        elif (target == "B'"):
            rotateLeft90(caseName, 'B')


def qrScan(imgs):
    sequence = ['U', 'R', 'F', 'D', 'L', 'B']
    result = []

    # Initialize QR_Code
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')

    # Load image
    # Convert grayscale
    for seq in sequence:
        src_img = imgs[seq]
        rows, cols = src_img.shape[:2]  
        for i in range(1, 5, 1):
            gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
            image = zbar.Image(cols, rows, 'Y800', gray_img.tostring())  
            scanResult = scanner.scan(image)
#            print "scanResult[%d]" % (scanResult)
            if (scanResult == 0):
                # Scan failed.
                src_img = rotateCenter(src_img)
            else:
                break

        for symbol in image:  
            result.append(symbol.data)

    return result

if __name__ == "__main__":
    # UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
    #caseName = '01000000000000000000'
    #caseName = '02c286df1bbd7923d1f7'
    #caseName = '038bc84b7b3f9681630f'
    #caseName = '04c0348a6aeca46e33af'
    #caseName = '05778a23f9eca28ff7e2'
    #caseName = '066a75f5d4895eb1d668'
    #caseName = '07f06a3ec2039c403953'
    #caseName = '08dbdb72757675be6bf6'
    #caseName = '105019f4e43866e664e2'
    #caseName = '11ed5b705e72e9fa2e57'
    #caseName = '12de86366ccad8ad3f0e'
    #caseName = '131c139206e8120f4e89'
    caseName = args[1]

    imgs = loadImageFiles(caseName)
    checkBaseColor(imgs)
    print "baseColors[%s]" % baseColors
    cubeCase = serialize(imgs)
    print "cubeCase[%s]" % cubeCase
    solveSeq = kociemba.solve(cubeCase)
    print "solveSeq[%s]" % solveSeq
    solve(caseName, solveSeq)
    imgs = loadImageFiles(caseName)
    urls = qrScan(imgs)
    with open("./urls.txt", "w") as file:
        for url in urls:
            file.write(url)
            file.write('\n')

