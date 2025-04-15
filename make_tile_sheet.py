from PIL import Image
import os
import math
import glob

"""
사용법:
1. 이 스크립트를 실행합니다: python tilesheet_creator.py
2. 이미지가 있는 폴더 경로를 입력합니다
3. 하위 폴더 탐색 여부를 선택합니다 (y/n)
4. 출력할 타일시트 파일 경로를 입력합니다
5. 각 타일의 너비와 높이를 픽셀 단위로 입력합니다
6. 타일시트 레이아웃 설정 여부를 선택합니다 (y/n)
   - 선택한 경우: 가로/세로 타일 수를 입력합니다 (자동 계산은 Enter)
"""

def create_tilesheet(source_dir, output_path, tile_width, tile_height, sheet_width=None, sheet_height=None, recursive=True):
    source_dir = os.path.abspath(source_dir)
    output_path = os.path.abspath(output_path)
    
    print(f"이미지 검색 경로: {source_dir}")
    
    image_files = []
    
    if recursive:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.lower().endswith(('.png', '.bmp')):
                    image_files.append(os.path.join(root, file))
    else:
        png_files = glob.glob(os.path.join(source_dir, "*.png"))
        bmp_files = glob.glob(os.path.join(source_dir, "*.bmp"))
        png_files_upper = glob.glob(os.path.join(source_dir, "*.PNG"))
        bmp_files_upper = glob.glob(os.path.join(source_dir, "*.BMP"))
        
        image_files = png_files + bmp_files + png_files_upper + bmp_files_upper
    
    if not image_files:
        print(f"오류: {source_dir}와 그 하위 폴더에서 이미지 파일을 찾을 수 없습니다.")
        print("지원되는 형식: .png, .PNG, .bmp, .BMP")
        return False
    
    print(f"총 {len(image_files)}개의 이미지 파일을 찾았습니다.")
    
    image_files.sort()
    
    num_images = len(image_files)
    
    if sheet_width is None and sheet_height is None:
        sheet_width = math.ceil(math.sqrt(num_images))
        sheet_height = math.ceil(num_images / sheet_width)
    elif sheet_width is None:
        sheet_width = math.ceil(num_images / sheet_height)
    elif sheet_height is None:
        sheet_height = math.ceil(num_images / sheet_width)
    
    final_width = sheet_width * tile_width
    final_height = sheet_height * tile_height
    
    tilesheet = Image.new('RGB', (final_width, final_height), (0, 0, 0))
    
    print(f"타일시트 생성 중: {sheet_width}x{sheet_height} 타일 ({final_width}x{final_height} 픽셀)")
    
    processed_images = []
    
    for index, img_path in enumerate(image_files):
        if index >= sheet_width * sheet_height:
            print(f"경고: 지정된 타일시트 크기를 초과했습니다. {len(image_files) - index}개 이미지가 포함되지 않았습니다.")
            break
            
        try:
            img = Image.open(img_path)
            img = img.convert('RGB')
            
            img_file = os.path.basename(img_path)
            
            if img.width != tile_width or img.height != tile_height:
                print(f"리사이즈: {img_file} ({img.width}x{img.height} -> {tile_width}x{tile_height})")
                img = img.resize((tile_width, tile_height), Image.LANCZOS)
            
            row = index // sheet_width
            col = index % sheet_width
            x = col * tile_width
            y = row * tile_height
            
            tilesheet.paste(img, (x, y))
            processed_images.append(img_path)
            print(f"처리 완료: {img_file} -> 위치 ({col}, {row})")
            
        except Exception as e:
            print(f"이미지 처리 오류 {img_path}: {e}")
    
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"출력 폴더 생성: {output_dir}")
        except Exception as e:
            print(f"출력 폴더 생성 오류: {e}")
            return False
    
    try:
        ext = os.path.splitext(output_path)[1].lower()
        if ext == '.bmp':
            tilesheet.save(output_path, 'BMP')
        elif ext in ['.jpg', '.jpeg']:
            tilesheet.save(output_path, 'JPEG', quality=95)
        elif ext == '.png':
            tilesheet.save(output_path, 'PNG')
        else:
            if not ext:
                output_path += '.bmp'
            tilesheet.save(output_path, 'BMP')
        
        print(f"\n타일시트 생성 완료: {output_path}")
        print(f"총 이미지: {len(image_files)}, 처리된 이미지: {len(processed_images)}")
        
        return True
    except Exception as e:
        print(f"타일시트 저장 오류: {e}")
        return False

if __name__ == "__main__":
    try:
        source_directory = input("이미지 파일이 있는 폴더 경로를 입력하세요: ").strip()
        source_directory = source_directory.strip('"\'')
        
        if not os.path.exists(source_directory):
            print(f"오류: 지정한 경로가 존재하지 않습니다: {source_directory}")
            input("\n프로그램을 종료하려면 아무 키나 누르세요...")
            exit()
        
        if not os.path.isdir(source_directory):
            print(f"오류: 지정한 경로가 폴더가 아닙니다: {source_directory}")
            input("\n프로그램을 종료하려면 아무 키나 누르세요...")
            exit()
        
        recursive_option = input("하위 폴더까지 모두 탐색하시겠습니까? (y/n): ").lower()
        recursive = recursive_option in ['y', 'yes']
        
        output_file = input("생성할 타일시트 파일 경로를 입력하세요 (예: C:\\output\\tilesheet.bmp): ").strip()
        output_file = output_file.strip('"\'')
        
        try:
            tile_width = int(input("각 타일의 너비(픽셀)를 입력하세요: "))
            tile_height = int(input("각 타일의 높이(픽셀)를 입력하세요: "))
        except ValueError:
            print("오류: 타일 크기는 숫자로 입력해야 합니다.")
            input("\n프로그램을 종료하려면 아무 키나 누르세요...")
            exit()
        
        sheet_layout = input("타일시트 레이아웃을 지정하시겠습니까? (y/n): ").lower()
        
        sheet_width = None
        sheet_height = None
        
        if sheet_layout in ['y', 'yes']:
            width_input = input("타일시트의 가로 타일 수를 입력하세요 (자동 계산은 Enter): ")
            if width_input.strip():
                try:
                    sheet_width = int(width_input)
                except ValueError:
                    print("오류: 가로 타일 수는 숫자로 입력해야 합니다. 자동 계산됩니다.")
                
            height_input = input("타일시트의 세로 타일 수를 입력하세요 (자동 계산은 Enter): ")
            if height_input.strip():
                try:
                    sheet_height = int(height_input)
                except ValueError:
                    print("오류: 세로 타일 수는 숫자로 입력해야 합니다. 자동 계산됩니다.")
        
        create_tilesheet(source_directory, output_file, tile_width, tile_height, sheet_width, sheet_height, recursive)
        
    except Exception as e:
        print(f"예상치 못한 오류가 발생했습니다: {e}")
        
    input("\n프로그램을 종료하려면 아무 키나 누르세요...")
