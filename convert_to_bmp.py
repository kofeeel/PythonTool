from PIL import Image
import os

def convert_png_to_bmp_recursive(source_dir, dest_dir=None, delete_original=False):
    # 대상 디렉토리가 지정되지 않았으면 소스 디렉토리와 동일하게 설정
    if dest_dir is None:
        dest_dir = source_dir
    
    # 변환된 파일 수 카운트
    converted_count = 0
    deleted_count = 0
    
    print(f"시작: {source_dir}의 모든 PNG 파일을 BMP로 변환합니다...")
    
    # 모든 파일과 하위 디렉토리 처리
    for root, dirs, files in os.walk(source_dir):
        # 상대 경로 계산
        rel_path = os.path.relpath(root, source_dir)
        
        # 현재 처리 중인 디렉토리에 대응하는 대상 디렉토리 생성
        if rel_path != ".":
            target_dir = os.path.join(dest_dir, rel_path)
        else:
            target_dir = dest_dir
            
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            print(f"폴더 생성: {target_dir}")
        
        # 현재 디렉토리의 PNG 파일들 처리
        for file in files:
            if file.lower().endswith(".png"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(target_dir, file.replace(".png", ".bmp").replace(".PNG", ".bmp"))
                
                try:
                    # PNG를 BMP로 변환
                    img = Image.open(input_path)
                    img = img.convert("RGB")  # 24비트 RGB로 변환
                    img.save(output_path, "BMP")
                    
                    converted_count += 1
                    print(f"변환 완료: {input_path} -> {output_path}")
                    
                    # 원본 파일 삭제 옵션이 켜져 있으면 삭제
                    if delete_original:
                        os.remove(input_path)
                        deleted_count += 1
                        print(f"원본 삭제: {input_path}")
                        
                except Exception as e:
                    print(f"변환 오류 {input_path}: {e}")
    
    print(f"\n변환 완료! 총 {converted_count}개 파일 변환됨.")
    if delete_original:
        print(f"총 {deleted_count}개 원본 PNG 파일 삭제됨.")

if __name__ == "__main__":
    # 사용자에게 최상위 디렉토리만 입력 받기
    source_directory = input("PNG 파일이 있는 최상위 폴더 경로를 입력하세요: ")
    
    # 사용자에게 입력받은 경로가 존재하는지 확인
    if not os.path.exists(source_directory):
        print(f"오류: {source_directory} 경로를 찾을 수 없습니다.")
        exit()
    
    # 출력 디렉토리 입력 (선택사항)
    dest_directory = input("BMP 파일을 저장할 폴더 경로를 입력하세요 (그냥 Enter 누르면 원본과 같은 폴더에 저장): ")
    if dest_directory.strip() == "":
        dest_directory = source_directory
    
    # 원본 삭제 여부 확인
    delete_option = input("변환 후 원본 PNG 파일을 삭제할까요? (y/n): ").lower()
    delete_original = delete_option == 'y' or delete_option == 'yes'
    
    if delete_original:
        confirm = input("주의: 원본 PNG 파일이 영구적으로 삭제됩니다. 계속하시겠습니까? (y/n): ").lower()
        if confirm != 'y' and confirm != 'yes':
            print("작업이 취소되었습니다.")
            exit()
    
    # 변환 실행
    convert_png_to_bmp_recursive(source_directory, dest_directory, delete_original)
    
    input("\n프로그램을 종료하려면 아무 키나 누르세요...")
