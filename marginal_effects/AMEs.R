#AME
options(scipen=999)
set.seed(42)
library(margins)

sim_binary_data = function(sample_size = 20, intercept = -0.3, beta_1 = 2, beta_2= -1.35) {
  x1 = rnorm(n = sample_size)
  x2 = rbinom(n = sample_size, size = 1, prob = 0.5)
  eta = intercept + beta_1 * x1+ beta_2 * x2
  p = 1 / (1 + exp(-eta))
  y = rbinom(n = sample_size, size = 1, prob = p)
  data.frame(y, x1, x2)}

dat = sim_binary_data()

model <- glm(y ~ x1 + x2, data = dat, family = 'binomial')

avg_margins <- function(x){
  coefficients <- coef(x)
  probabilities <- x$fitted.values*(1-x$fitted.values)
  ames <- vector(mode = "list", length = length(coefficients))
  for(i in 1:length(coefficients)){
    ames[i:i] <- mean(coefficients[i] * probabilities)
  }
  names(ames) <- names(coeffs)
  ames <- data.frame(ames)
  return(ames)
}


ame <- function(x){
  mfx <- coef(x) * mean(x$fitted.values * (1-x$fitted.values))
  return(mfx)
}

summary(margins(model))
ame(model)

#LPM 

lm(y ~ x1 + x2, data = dat)


coefficients <- coef(model)

probabilities <- model$fitted.values * (1-model$fitted.values)
probs2 <- dlogis(predict(model))

round(probs2, 5) == round(probabilities, 5)

library(pracma)


t(coefficients) * matrix(probabilities)

dlogis(model)
