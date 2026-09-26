set.seed(415)
# 이원분산분석용: 성별 x 학교유형 (11장) — 원고의 설계를 그대로 따름
cells <- expand.grid(gender = c("남","여"),
                     school = c("남녀공학/분반","남녀공학/합반","단성학교"))
# 셀 평균을 이렇게 잡으면 상호작용이 드러난다.
# 남학생은 단성학교에서 크게 오르지만 여학생은 그렇지 않다.
mu <- c(67, 70,   73, 76,   83, 75)
rows <- do.call(rbind, lapply(seq_len(nrow(cells)), function(i)
  data.frame(gender = cells$gender[i], school = cells$school[i],
             score = round(rnorm(18, mu[i], 6.2), 1))))
write.csv(rows, "books/01-basic-statistics/data/twoway.csv", row.names = FALSE)
cat("twoway.csv 생성:", nrow(rows), "행\n")
