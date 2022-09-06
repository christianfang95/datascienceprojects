library(DescTools)
library(ggplot2)
library(gridExtra)
library(dplyr)

#Set seed
set.seed(47549)

#Simulate the data (https://book.stat420.org/logistic-regression.html)
sim_logistic_data = function(sample_size = 1000, beta_0 = -0.20, beta_1 = -0.32, beta_2= 3.5, beta_3 = 1.5) {
  x = rnorm(n = sample_size)
  eta = beta_0 + beta_1 * x + (beta_2 * beta_1) * x + beta_2 * x + beta_3 * x
  p = 1 / (1 + exp(-eta))
  y = rbinom(n = sample_size, size = 1, prob = p)
  data.frame(y, x)}
  
#Generate data and view head
example_data = sim_logistic_data()
head(example_data)

#Plot LPM and logistic regression
fit_lpm  = lm(y ~ x, data = example_data)
fit_glm = glm(y ~ x, data = example_data, family = binomial(link = "logit"))

# Plot predictions
plot(y ~ x, data = example_data, 
     pch = 20, ylab = "Estimated Probability", 
     main = "LPM vs Logistic Regression")
grid()
abline(fit_lpm, col = "darkorange")
curve(predict(fit_glm, data.frame(x), type = "response"), 
      add = TRUE, col = "dodgerblue", lty = 2)
legend("topleft", c("LPM", "Logistic Regression", "Data"), lty = c(1, 2, 0),       
       pch = c(NA, NA, 20), lwd = 2, col = c("darkorange", "dodgerblue", "black")) 


#predictions from logistic regression
predicted_labels_glm <- as.numeric(predict(fit_glm, data.frame(example_data), type = "response"))
actual_labels_glm <- as.numeric(example_data$y)

#predictions from LPM
predicted_labels_lpm <- as.numeric(predict(fit_lpm, data.frame(example_data)))
actual_labels_lpm <- as.numeric(example_data$y)

#thresholds
thresholds <- seq(from = 0.00001, to = 1, by = 0.00001)
#Number of positive and negative examples in the data
P <- sum(actual_labels_glm == 1)
N <- sum(actual_labels_glm == 0)
FPR <- rep(0, length(thresholds))
TPR <- rep(0, length(thresholds))
#Execute code below n times
for (i in 1:length(thresholds)) {
TP <- 0
FP <- 0
for (row in 1:length(predicted_labels_glm)) {
  if ((predicted_labels_glm[[row]] >= thresholds[[i]]) & (actual_labels_glm[[row]] == 1)){TP <- TP + 1}
  if ((predicted_labels_glm[[row]] >= thresholds[[i]]) & (actual_labels_glm[[row]] == 0)){FP <- FP + 1}
  FPR[[i]] <- (FP/N)
  TPR[[i]] <- (TP/P)
}
}
df_logit <- data.frame(FPR, TPR)

#FOR THE LPM
for (i in 1:length(thresholds)) {
  TP <- 0
  FP <- 0
  for (row in 1:length(predicted_labels_lpm)) {
    if ((predicted_labels_lpm[[row]] >= thresholds[[i]]) & (actual_labels_lpm[[row]] == 1)){TP <- TP + 1}
    if ((predicted_labels_lpm[[row]] >= thresholds[[i]]) & (actual_labels_lpm[[row]] == 0)){FP <- FP + 1}
    FPR[[i]] <- (FP/N)
    TPR[[i]] <- (TP/P)
  }
}
df_lpm <- data.frame(FPR, TPR)

#Calculate AUC
AUC_logit <- AUC(df_logit$FPR, df_logit$TPR)
AUC_lpm <- AUC(df_lpm$FPR, df_lpm$TPR)


#Set titles for figures
title_logit = paste0("ROC of Logistic Regression, AUC=", round(AUC_logit, 3), "")
title_lpm = paste0("ROC of undajusted LPM, AUC=", round(AUC_lpm, 3), "")

#Plot
plot1 <- ggplot(df_logit, aes(x=FPR, y=TPR)) + geom_line() +
        labs(title = title_logit) + 
        theme(plot.title = element_text(size=8)) + 
        geom_abline(slope=1, intercept=0, linetype = "dashed", size = 0.4) +
        xlim(0, 1) + 
        ylim(0, 1) 
plot2 <- ggplot(df_lpm, aes(x=FPR, y=TPR)) + 
        geom_line() + 
        labs(title = title_lpm) + 
        theme(plot.title = element_text(size=10)) + 
        xlim(0, 1) + 
        ylim(0, 1) +
        geom_abline(slope=1, intercept=0, linetype = "dashed", size = 0.4)
grid.arrange(plot1, plot2, ncol=2)

#Plot for LPM looks wonky because of nonsense predictions (ROC cannot be calculated if predictions are out of range)

#fix nonsense predictions
predicted_labels_lpm_fixed <- case_when(predicted_labels_lpm < 0 ~ 0.10, 
                                        predicted_labels_lpm > 0 & predicted_labels_lpm < 1 ~ predicted_labels_lpm,
                                        predicted_labels_lpm > 1 ~ 0.90)
#Calculate FPR and TPR again 
for (i in 1:length(thresholds)) {
  TP <- 0
  FP <- 0
  for (row in 1:length(predicted_labels_lpm_fixed)) {
    if ((predicted_labels_lpm_fixed[[row]] >= thresholds[[i]]) & (actual_labels_lpm[[row]] == 1)){TP <- TP + 1}
    if ((predicted_labels_lpm_fixed[[row]] >= thresholds[[i]]) & (actual_labels_lpm[[row]] == 0)){FP <- FP + 1}
    FPR[[i]] <- (FP/N)
    TPR[[i]] <- (TP/P)
  }
}
df_lpmadjusted <- data.frame(FPR, TPR)

#Recalculate AUC
AUC_lpm_adjusted <- AUC(df_lpmadjusted$FPR, df_lpmadjusted$TPR)
#Adjust figure title
title_lpm_adjusted = paste0("ROC of adjusted LPM, AUC=", round(AUC_lpm_adjusted, 3), "")
#Plot figures again
plot2a <- ggplot(df_lpmadjusted, aes(x=FPR, y=TPR)) + 
  geom_line() + 
  labs(title = title_lpm_adjusted) + 
  theme(plot.title = element_text(size=10)) + 
  xlim(0, 1) + 
  ylim(0, 1) +
  geom_abline(slope=1, intercept=0, linetype = "dashed", size = 0.4)
grid.arrange(plot1, plot2, plot2a, ncol=3)







