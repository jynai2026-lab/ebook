# 2권 예제 자료 생성 스크립트
#
#   Rscript books/02-regression/data/make-data.R
#
# 직장인 300명 설문(가상 자료). 1장부터 11장까지 같은 자료를 씁니다.
# 척도 점수는 문항 평균(1~5점)이며, 문항 수에 맞춰 끝자리를 맞췄습니다.

set.seed(2026)
n <- 300

# 인구학적 변수
gender <- sample(c("남", "여"), n, replace = TRUE, prob = c(.52, .48))
age    <- pmin(pmax(round(rnorm(n, 37, 7.5)), 24), 58)
tenure <- pmin(pmax(round((age - 26) * 0.62 + rnorm(n, 0, 2.8)), 0), age - 22)
pos_score <- tenure + rnorm(n, 0, 2.2)
position <- ifelse(pos_score < 4.5, "사원", ifelse(pos_score < 10, "대리", "과장이상"))

# 잠재 점수 (표준화)
z <- function() rnorm(n)
z_stress   <- z()
z_workload <- .88 * z_stress + sqrt(1 - .88^2) * z()
z_support  <- -.22 * z_stress + sqrt(1 - .22^2) * z()
z_efficacy <- -.12 * z_stress + .20 * z_support + .97 * z()
z_burnout  <- .44 * z_stress - .24 * z_support - .20 * z_efficacy -
              .17 * z_stress * z_support +
              .09 * (gender == "여") - .010 * (age - 37) + .70 * z()
z_turnover <- .46 * z_burnout + .16 * z_stress - .08 * z_support + .80 * z()
z_satis    <- -.40 * z_burnout + .18 * z_support +
              .25 * (position == "대리") + .55 * (position == "과장이상") + .80 * z()

# 1~5점 척도로 옮기고 문항 수에 맞춰 반올림
likert <- function(zv, m, s, items) {
  x <- m + s * (zv - mean(zv)) / sd(zv)
  x <- round(x * items) / items
  round(pmin(pmax(x, 1), 5), 2)
}
stress       <- likert(z_stress,   3.08, .62, 6)
workload     <- likert(z_workload, 3.31, .68, 5)
support      <- likert(z_support,  3.52, .60, 8)
efficacy     <- likert(z_efficacy, 3.61, .55, 6)
burnout      <- likert(z_burnout,  2.86, .68, 9)
turnover     <- likert(z_turnover, 2.71, .84, 4)
satisfaction <- likert(z_satis,    3.27, .66, 5)

# 1년 뒤 실제 퇴사 여부 (0 = 재직, 1 = 퇴사)
eta  <- -1.75 + 1.05 * (turnover - 2.71) / .84 - .45 * (satisfaction - 3.27) / .66
quit <- rbinom(n, 1, plogis(eta))

survey <- data.frame(id = 1:n, gender, age, tenure, position,
                     stress, workload, support, efficacy,
                     burnout, satisfaction, turnover, quit)
write.csv(survey, "books/02-regression/data/survey.csv", row.names = FALSE)
