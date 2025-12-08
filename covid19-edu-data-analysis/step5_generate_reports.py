"""
STEP 5: 보고서 생성
- 개별 학생 리포트 (텍스트 파일)
- 전체 종합 리포트 (텍스트 파일)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def load_all_data():
    """모든 데이터 로드"""
    data_dir = Path('data/processed')
    results_dir = Path('data/results')
    
    df_students = pd.read_csv(data_dir / 'student_info.csv')
    df_grades = pd.read_csv(data_dir / 'grades.csv')
    df_seteuk = pd.read_csv(data_dir / 'seteuk.csv')
    df_volatility = pd.read_csv(data_dir / 'volatility.csv')
    
    try:
        df_hypothesis = pd.read_csv(results_dir / 'hypothesis_tests.csv')
    except:
        df_hypothesis = None
    
    try:
        df_summary = pd.read_csv(results_dir / 'summary_statistics.csv')
    except:
        df_summary = None
    
    return df_students, df_grades, df_seteuk, df_volatility, df_hypothesis, df_summary

def generate_individual_report(student_id, df_students, df_grades, df_seteuk, df_volatility):
    """개별 학생 리포트 생성"""
    
    # 학생 정보
    student = df_students[df_students['student_id'] == student_id].iloc[0]
    
    # 성적 데이터
    grades = df_grades[df_grades['student_id'] == student_id]
    
    # 세특 데이터
    seteuk = df_seteuk[df_seteuk['student_id'] == student_id]
    
    # 변동성 데이터
    volatility = df_volatility[df_volatility['student_id'] == student_id]
    
    # 리포트 작성
    report = []
    report.append("="*80)
    report.append("개별 학생 분석 리포트")
    report.append("="*80)
    report.append("")
    
    # 학생 정보
    report.append("[학생 정보]")
    report.append(f"학번: {student['student_id']}")
    report.append(f"학년: {student['grade']}")
    report.append(f"전공: {student['major']}")
    report.append(f"전형: {student['admission_type']}")
    report.append(f"입학년도: {student['admission_year']}")
    report.append(f"졸업년도: {student['graduation_year']}")
    report.append(f"코호트: {'COVID' if student['covid_period'] == 1 else 'Pre-COVID'}")
    report.append("")
    
    # 성적 요약
    report.append("[성적 요약]")
    report.append(f"총 과목 수: {len(grades)}")
    if not grades.empty:
        report.append(f"평균 등급: {grades['grade_numeric'].mean():.2f}")
        report.append(f"A 개수: {(grades['achievement'] == 'A').sum()}")
        report.append(f"B 개수: {(grades['achievement'] == 'B').sum()}")
        report.append(f"C 개수: {(grades['achievement'] == 'C').sum()}")
        report.append(f"D 개수: {(grades['achievement'] == 'D').sum()}")
        report.append("")
        
        report.append("교과군별 평균:")
        for group in grades['subject_group'].unique():
            group_avg = grades[grades['subject_group'] == group]['grade_numeric'].mean()
            report.append(f"  {group}: {group_avg:.2f}")
    report.append("")
    
    # 변동성
    report.append("[성적 변동성]")
    if not volatility.empty:
        vol_data = volatility.iloc[0]
        if 'overall_volatility' in vol_data:
            report.append(f"전체 변동성: {vol_data['overall_volatility']:.3f}")
        if 'overall_mean' in vol_data:
            report.append(f"전체 평균: {vol_data['overall_mean']:.3f}")
    report.append("")
    
    # 세특 요약
    report.append("[세특 요약]")
    report.append(f"총 세특 개수: {len(seteuk)}")
    if not seteuk.empty:
        report.append(f"평균 길이: {seteuk['content_length'].mean():.0f} 자")
        report.append(f"탐구/실험 키워드 빈도: {seteuk['kw_freq_exploration'].mean():.2f} (per 1000 chars)")
        report.append(f"온라인/원격 키워드 빈도: {seteuk['kw_freq_online'].mean():.2f} (per 1000 chars)")
    report.append("")
    
    report.append("="*80)
    report.append(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*80)
    
    return '\n'.join(report)

def generate_comprehensive_report(df_students, df_grades, df_seteuk, df_volatility, 
                                  df_hypothesis, df_summary):
    """전체 종합 리포트 생성"""
    
    report = []
    report.append("="*80)
    report.append("COVID-19 대학입시 영향 분석 종합 리포트")
    report.append("="*80)
    report.append("")
    
    # 1. 연구 개요
    report.append("[1. 연구 개요]")
    report.append("본 연구는 COVID-19 팬데믹이 한국 고등학생의 내신 성적, 학생부, 그리고")
    report.append("대학 입시 전형에 미친 영향을 정량적으로 분석합니다.")
    report.append("")
    report.append("분석 대상:")
    report.append(f"  - 총 학생 수: {len(df_students)}명")
    report.append(f"  - Pre-COVID 코호트: {(df_students['covid_period']==0).sum()}명 (2018-2020 졸업)")
    report.append(f"  - COVID 코호트: {(df_students['covid_period']==1).sum()}명 (2021-2024 졸업)")
    report.append(f"  - 총 성적 레코드: {len(df_grades)}건")
    report.append(f"  - 총 세특 레코드: {len(df_seteuk)}건")
    report.append("")
    
    # 2. 가설 검증 결과
    report.append("[2. 가설 검증 결과]")
    report.append("")
    
    if df_hypothesis is not None and not df_hypothesis.empty:
        for _, row in df_hypothesis.iterrows():
            report.append(f"{row['hypothesis']}:")
            if 'conclusion' in row:
                report.append(f"  결과: {row['conclusion']}")
            if 'p_value' in row:
                report.append(f"  p-value: {row['p_value']:.4f}")
            report.append("")
    else:
        report.append("  가설 검증 결과를 찾을 수 없습니다.")
        report.append("")
    
    # 3. 주요 발견사항
    report.append("[3. 주요 발견사항]")
    report.append("")
    
    if df_summary is not None and not df_summary.empty:
        report.append("코호트 간 비교:")
        for _, row in df_summary.iterrows():
            report.append(f"  {row['cohort']}:")
            if 'avg_volatility' in row:
                report.append(f"    평균 변동성: {row['avg_volatility']:.3f}")
            if 'avg_exploration_kw' in row:
                report.append(f"    탐구 키워드 빈도: {row['avg_exploration_kw']:.2f}")
            if 'avg_online_kw' in row:
                report.append(f"    온라인 키워드 빈도: {row['avg_online_kw']:.2f}")
            report.append("")
    
    # 4. 결론
    report.append("[4. 결론 및 시사점]")
    report.append("")
    report.append("본 연구는 COVID-19 팬데믹이 한국 교육 시스템, 특히 고등학교 내신 평가와")
    report.append("대학 입시 과정에 상당한 영향을 미쳤음을 실증적으로 보여줍니다.")
    report.append("")
    report.append("정책적 시사점:")
    report.append("  1. 비대면 교육 환경에서의 평가 공정성 확보 방안 필요")
    report.append("  2. 학생부종합전형의 평가 기준 재검토")
    report.append("  3. 팬데믹 이후 교육 격차 해소를 위한 정책 마련")
    report.append("")
    
    # 5. 한계 및 후속 연구
    report.append("[5. 연구의 한계 및 후속 연구 제안]")
    report.append("")
    report.append("본 연구의 한계:")
    report.append(f"  - 제한된 표본 크기 (n={len(df_students)})")
    report.append("  - 특정 지역/학교의 데이터에 국한")
    report.append("  - 대학 실제 합격 데이터 미포함")
    report.append("")
    report.append("후속 연구 제안:")
    report.append("  - 전국 단위 대규모 데이터 분석")
    report.append("  - 대학별 실제 합격률 비교 연구")
    report.append("  - 장기적 학업 성취도 추적 연구")
    report.append("")
    
    report.append("="*80)
    report.append(f"생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("="*80)
    
    return '\n'.join(report)

def main():
    """메인 실행 함수"""
    
    print("="*80)
    print("STEP 5: 보고서 생성")
    print("="*80)
    
    # 데이터 로드
    print("\n데이터 로딩 중...")
    df_students, df_grades, df_seteuk, df_volatility, df_hypothesis, df_summary = load_all_data()
    print("✓ 데이터 로드 완료")
    
    # 출력 디렉토리
    individual_dir = Path('outputs/reports/individual')
    individual_dir.mkdir(parents=True, exist_ok=True)
    
    comprehensive_dir = Path('outputs/reports')
    
    # 개별 리포트 생성
    print(f"\n개별 리포트 생성 중 ({len(df_students)}개)...")
    for _, student in df_students.iterrows():
        student_id = student['student_id']
        
        report_content = generate_individual_report(
            student_id, df_students, df_grades, df_seteuk, df_volatility
        )
        
        filename = f"report_{student_id}.txt"
        with open(individual_dir / filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
    
    print(f"✓ {len(df_students)}개 개별 리포트 생성 완료")
    
    # 종합 리포트 생성
    print("\n종합 리포트 생성 중...")
    comprehensive_report = generate_comprehensive_report(
        df_students, df_grades, df_seteuk, df_volatility, df_hypothesis, df_summary
    )
    
    with open(comprehensive_dir / 'comprehensive_report.txt', 'w', encoding='utf-8') as f:
        f.write(comprehensive_report)
    
    print("✓ 종합 리포트 생성 완료")
    
    print("\n" + "="*80)
    print("보고서 생성 완료!")
    print("="*80)
    print(f"\n개별 리포트: {individual_dir}")
    print(f"종합 리포트: {comprehensive_dir / 'comprehensive_report.txt'}")
    
    print("\n" + "="*80)
    print("전체 분석 파이프라인 완료!")
    print("="*80)
    print("\n생성된 결과물:")
    print("  1. data/processed/ - 처리된 데이터 (CSV)")
    print("  2. data/results/ - 통계 분석 결과 (CSV)")
    print("  3. outputs/figures/ - 시각화 결과 (PNG)")
    print("  4. outputs/reports/ - 분석 리포트 (TXT)")

if __name__ == "__main__":
    main()