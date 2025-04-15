from PIL import Image
import os

def change_background_color(input_path, output_path, old_color=(0, 0, 0), new_color=(255, 0, 255), delete_original=False):
    try:
        # 입력 파일이 존재하는지 확인
        if not os.path.isfile(input_path):
            print(f"오류: 입력 파일이 존재하지 않거나 폴더입니다: {input_path}")
            return False
        
        # 출력 경로가 디렉토리인지 확인하고, 디렉토리라면 파일명 추가
        if os.path.isdir(output_path):
            base_name = os.path.basename(input_path)
            output_path = os.path.join(output_path, f"magenta_{base_name}")
            print(f"출력 경로가 폴더이므로 파일명을 자동 생성합니다: {output_path}")
        
        # 출력 디렉토리가 있는지 확인하고 없으면 생성
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"출력 폴더를 생성했습니다: {output_dir}")
        
        # 이미지 파일 열기
        print(f"이미지 파일 열기: {input_path}")
        image = Image.open(input_path)
        
        # RGB 모드로 변환
        image = image.convert('RGB')
        
        # 픽셀 데이터 가져오기
        pixels = image.load()
        width, height = image.size
        
        # 각 픽셀을 확인하여 배경색 변경
        print("배경색 변경 중...")
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                # 기존 배경색과 일치하면 마젠타로 변경
                if pixel[0] == old_color[0] and pixel[1] == old_color[1] and pixel[2] == old_color[2]:
                    pixels[x, y] = new_color
        
        # 변경된 이미지 저장
        print(f"변경된 이미지 저장 중: {output_path}")
        
        # 파일 확장자 확인
        _, ext = os.path.splitext(output_path)
        if not ext:
            output_path += ".bmp"
            print(f"확장자가 없어 .bmp를 추가했습니다: {output_path}")
        
        image.save(output_path)
        print(f"배경색이 {old_color}에서 {new_color}로 변경되어 {output_path}에 저장되었습니다.")
        
        # 원본 파일 삭제 (옵션이 켜져 있을 경우)
        if delete_original and input_path != output_path:
            try:
                os.remove(input_path)
                print(f"원본 파일을 삭제했습니다: {input_path}")
            except Exception as e:
                print(f"원본 파일 삭제 중 오류 발생: {e}")
        
        return True
    
    except Exception as e:
        print(f"오류 발생: {e}")
        print(f"입력 파일: {input_path}")
        print(f"출력 파일: {output_path}")
        return False

if __name__ == "__main__":
    # 사용자 입력 받기
    input_file = input("기존 타일시트 파일 경로를 입력하세요: ").strip().strip('"\'')
    
    if not os.path.exists(input_file):
        print(f"오류: 입력 파일 또는 폴더가 존재하지 않습니다: {input_file}")
        input("\n프로그램을 종료하려면 아무 키나 누르세요...")
        exit()
    
    # 기존 배경색 입력 (기본값: 검은색)
    try:
        print("기존 배경색을 입력하세요 (기본값: 0,0,0 - 검은색):")
        r = input("R (0-255): ").strip() or "0"
        g = input("G (0-255): ").strip() or "0"
        b = input("B (0-255): ").strip() or "0"
        
        old_color = (int(r), int(g), int(b))
    except ValueError:
        print("오류: 색상 값은 0-255 사이의 숫자여야 합니다. 기본값(0,0,0)을 사용합니다.")
        old_color = (0, 0, 0)
    
    # 출력 파일 경로
    output_file = input("저장할 파일 경로를 입력하세요 (기본값: 원본 파일명_magenta): ").strip().strip('"\'')
    
    if not output_file:
        base_name, ext = os.path.splitext(input_file)
        output_file = f"{base_name}_magenta{ext}"
        if not ext:
            output_file += ".bmp"
    
    # 원본 삭제 여부 확인
    delete_option = input("변환 후 원본 파일을 삭제하시겠습니까? (y/n): ").lower()
    delete_original = delete_option == 'y' or delete_option == 'yes'
    
    if delete_original and input_file == output_file:
        print("경고: 입력 파일과 출력 파일이 같으므로 원본이 삭제되지 않습니다.")
        delete_original = False
    
    if delete_original:
        confirm = input("주의: 원본 파일이 영구적으로 삭제됩니다. 계속하시겠습니까? (y/n): ").lower()
        delete_original = confirm == 'y' or confirm == 'yes'
        
        if not delete_original:
            print("원본 파일 삭제를 취소했습니다.")
    
    # 배경색 변경
    change_background_color(input_file, output_file, old_color, (255, 0, 255), delete_original)
    
    input("\n프로그램을 종료하려면 아무 키나 누르세요...")
