# 그림용 자료를 만든다. 그림은 tools/fig2_*.py 가 이 JSON을 읽어 그린다.
#
#   Rscript books/02-regression/r/figdata.R
#
# 책에 실린 숫자와 그림이 같은 자료에서 나오도록, 그림의 점·선도 R이 계산한다.
suppressPackageStartupMessages(library(jsonlite))
setwd(file.path(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(FALSE), value = TRUE)))), ".."))
d <- read.csv("data/survey.csv")
d$position <- factor(d$position, levels = c("사원", "대리", "과장이상"))
out <- function(x, name) write_json(x, file.path("figdata", name), digits = 6, auto_unbox = TRUE)

# ---- 1장
out(list(x = d$stress, y = d$burnout, mx = mean(d$stress), my = mean(d$burnout),
         r = cor(d$stress, d$burnout)), "ch01-stress-burnout.json")
out(lapply(1:4, function(i) list(x = anscombe[[i]], y = anscombe[[i + 4]],
                                 r = cor(anscombe[[i]], anscombe[[i + 4]]))), "ch01-anscombe.json")
out(list(x = d$tenure, y = d$satisfaction, g = as.character(d$position),
         r = cor(d$tenure, d$satisfaction),
         within = sapply(split(d, d$position), function(g) cor(g$tenure, g$satisfaction)),
         gmx = tapply(d$tenure, d$position, mean), gmy = tapply(d$satisfaction, d$position, mean)),
    "ch01-third.json")

# ---- 2장
fit <- lm(burnout ~ stress, d)
grid <- seq(1.2, 4.6, by = .05)
ci <- predict(fit, data.frame(stress = grid), interval = "confidence")
pi <- predict(fit, data.frame(stress = grid), interval = "prediction")
out(list(x = d$stress, y = d$burnout, b0 = coef(fit)[[1]], b1 = coef(fit)[[2]],
         fitted = unname(fitted(fit)), grid = grid,
         ci_lo = ci[, "lwr"], ci_hi = ci[, "upr"], pi_lo = pi[, "lwr"], pi_hi = pi[, "upr"]),
    "ch02-fit.json")
cat("figdata 완료\n")
