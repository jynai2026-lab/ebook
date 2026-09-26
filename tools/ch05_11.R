suppressPackageStartupMessages({library(car); library(effectsize); library(psych)})

cat("===== 8장 종속표본 t-검정 =====\n")
pp <- read.csv("books/01-basic-statistics/data/prepost.csv")
cat(sprintf("사전 M=%.3f SD=%.3f / 사후 M=%.3f SD=%.3f\n",
    mean(pp$pre), sd(pp$pre), mean(pp$post), sd(pp$post)))
cat(sprintf("두 점수의 상관 r=%.3f\n", cor(pp$pre, pp$post)))
d <- pp$post - pp$pre
cat(sprintf("차이점수 M=%.3f SD=%.3f\n", mean(d), sd(d)))
print(t.test(pp$post, pp$pre, paired = TRUE))
cat("Cohen's d (차이점수 기준):", round(mean(d)/sd(d), 3), "\n")
cat("\n-- 독립표본으로 잘못 돌리면 --\n")
it <- t.test(pp$post, pp$pre, paired = FALSE, var.equal = TRUE)
cat(sprintf("t=%.3f df=%.0f p=%.4f  (대응 무시 시)\n", it$statistic, it$parameter, it$p.value))

cat("\n\n===== 9장 일원분산분석 =====\n")
tc <- read.csv("books/01-basic-statistics/data/teaching.csv")
tc$method <- factor(tc$method)
print(round(sapply(split(tc$score, tc$method), function(x) c(n=length(x), M=mean(x), SD=sd(x))), 2))
cat("\n-- Levene --\n"); print(leveneTest(score ~ method, data = tc))
fit <- aov(score ~ method, data = tc)
cat("\n-- ANOVA --\n"); print(summary(fit))
ss <- summary(fit)[[1]][["Sum Sq"]]
cat(sprintf("\nSSB=%.2f SSW=%.2f SST=%.2f  eta2=%.4f\n", ss[1], ss[2], sum(ss), ss[1]/sum(ss)))
print(eta_squared(fit)); print(omega_squared(fit))

cat("\n\n===== 10장 다중비교 =====\n")
cat("-- Tukey HSD --\n"); print(TukeyHSD(fit))
cat("\n-- Bonferroni --\n")
print(pairwise.t.test(tc$score, tc$method, p.adjust.method = "bonferroni"))
cat("\n-- 보정 없음(LSD) --\n")
print(pairwise.t.test(tc$score, tc$method, p.adjust.method = "none"))
cat("\n-- 제1종 오류 누적 --\n")
for (k in c(2,3,4,5,6)) {
  cmp <- choose(k,2); cat(sprintf("집단 %d개 -> 비교 %d회 -> 최소 1회 오류 확률 %.4f\n",
      k, cmp, 1 - 0.95^cmp))
}
