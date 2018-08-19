# Generated by Django 2.1 on 2018-08-19 11:05

from django.db import migrations, models
import tracker.models.setting


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='duration_format',
            field=models.PositiveSmallIntegerField(choices=[(tracker.models.setting.DurationFormat(1), 'Classic (3:45)'), (tracker.models.setting.DurationFormat(2), 'Decimal (3.75)')], default=tracker.models.setting.DurationFormat(1)),
        ),
        migrations.AddField(
            model_name='setting',
            name='locale',
            field=models.CharField(choices=[('af', 'Afrikaans'), ('ar', 'العربيّة'), ('ast', 'asturianu'), ('az', 'Azərbaycanca'), ('be', 'беларуская'), ('bg', 'български'), ('bn', 'বাংলা'), ('br', 'brezhoneg'), ('bs', 'bosanski'), ('ca', 'català'), ('cs', 'česky'), ('cy', 'Cymraeg'), ('da', 'dansk'), ('de', 'Deutsch'), ('dsb', 'dolnoserbski'), ('el', 'Ελληνικά'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'español'), ('es-ar', 'español de Argentina'), ('es-co', 'español de Colombia'), ('es-mx', 'español de Mexico'), ('es-ni', 'español de Nicaragua'), ('es-ve', 'español de Venezuela'), ('et', 'eesti'), ('eu', 'Basque'), ('fa', 'فارسی'), ('fi', 'suomi'), ('fr', 'français'), ('fy', 'frysk'), ('ga', 'Gaeilge'), ('gd', 'Gàidhlig'), ('gl', 'galego'), ('he', 'עברית'), ('hi', 'Hindi'), ('hr', 'Hrvatski'), ('hsb', 'hornjoserbsce'), ('hu', 'Magyar'), ('ia', 'Interlingua'), ('io', 'ido'), ('id', 'Bahasa Indonesia'), ('is', 'Íslenska'), ('it', 'italiano'), ('ja', '日本語'), ('ka', 'ქართული'), ('kab', 'taqbaylit'), ('kk', 'Қазақ'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', '한국어'), ('lb', 'Lëtzebuergesch'), ('lt', 'Lietuviškai'), ('lv', 'latviešu'), ('mk', 'Македонски'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'मराठी'), ('my', 'မြန်မာဘာသာ'), ('nb', 'norsk (bokmål)'), ('ne', 'नेपाली'), ('nl', 'Nederlands'), ('nn', 'norsk (nynorsk)'), ('no', 'norsk'), ('os', 'Ирон'), ('pa', 'Punjabi'), ('pl', 'polski'), ('pt', 'Português'), ('pt-br', 'Português Brasileiro'), ('ro', 'Română'), ('ru', 'Русский'), ('sk', 'Slovensky'), ('sl', 'Slovenščina'), ('sq', 'shqip'), ('sr', 'српски'), ('sr-latn', 'srpski (latinica)'), ('sv', 'svenska'), ('sw', 'Kiswahili'), ('ta', 'தமிழ்'), ('te', 'తెలుగు'), ('th', 'ภาษาไทย'), ('tr', 'Türkçe'), ('tt', 'Татарча'), ('udm', 'Удмурт'), ('uk', 'Українська'), ('ur', 'اردو'), ('vi', 'Tiếng Việt'), ('zh-hans', '简体中文'), ('zh-hant', '繁體中文')], default='en', max_length=10),
        ),
    ]
