df <- read.csv("sample_data.csv")
df$gender <- factor(df$gender, levels=c(1,2), labels=c("남성","여성"))
m <- split(df$selfesteem, df$gender)

out <- list()
for (g in names(m)) {
  d <- density(m[[g]], from = 1, to = 5.2, n = 120)
  out[[g]] <- list(x = d$x, y = d$y,
                   mean = mean(m[[g]]), sd = sd(m[[g]]),
                   q = as.numeric(quantile(m[[g]], c(.25,.5,.75))),
                   min = min(m[[g]]), max = max(m[[g]]))
}
# 간단한 JSON 직접 출력 (jsonlite 없이)
cat("{\n")
for (i in seq_along(out)) {
  g <- names(out)[i]; o <- out[[g]]
  cat(sprintf('"%s": {"x":[%s],"y":[%s],"mean":%f,"sd":%f,"q":[%s],"min":%f,"max":%f}%s\n',
    ifelse(g=="남성","male","female"),
    paste(round(o$x,4), collapse=","), paste(round(o$y,5), collapse=","),
    o$mean, o$sd, paste(round(o$q,3), collapse=","), o$min, o$max,
    ifelse(i < length(out), ",", "")))
}
cat("}\n")
