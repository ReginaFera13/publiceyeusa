from django.db import models
from django.core import validators as v
from user_app.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    display_name = models.CharField(validators=[v.MinLengthValidator(3), v.MaxLengthValidator(50)], null=True, blank=True)

# TODO: add political party affiliation app; one user, many affiliations; kinda like interest categories in ChangeMate app

# Major Parties
# Democratic Party
# Republican Party
# Minor and Third Parties
# Libertarian Party
# Green Party
# Constitution Party
# American Independent Party
# Peace and Freedom Party
# Working Families Party
# Independence Party of America
# Reform Party
# American Solidarity Party
# Unity Party of America
# Modern Whig Party
# State-Specific and Regional Parties
# Alaskan Independence Party
# California National Party
# New York State Right to Life Party
# Vermont Progressive Party
# Rhode Island Moderate Party
# Independent American Party (various states)
# Other Notable Political Affiliations
# Progressive Party
# Socialist Party USA
# Party for Socialism and Liberation
# American Party
# Justice Party
# Natural Law Party
# Prohibition Party
# Transhumanist Party
# Pirate Party
# American Heritage Party
# U.S. Marijuana Party
# Veterans Party of America
# Conservative Party USA
# America First Party
# Communist Party USA
# American Freedom Party
# Christian Liberty Party
# Citizens Party of the United States
# Non-Affiliated and Other Designations
# Independent
# Unaffiliated
# Nonpartisan