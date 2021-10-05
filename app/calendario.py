from .models import HistoricoHorarioModel
import datetime
from calendar import HTMLCalendar

month_name = ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro']
day_abbr = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']

class Calendar(HTMLCalendar):
    
    
    def __init__(self,ano, mes, usuario):

       
        self.ano = ano
        self.mes = mes
        self.usuario = usuario
        self.data_atual = datetime.date.today()
        super(Calendar,self).__init__()

    
    def formatday(self, dia):
        
        if dia != 0:
            
            data = HistoricoHorarioModel.objects.all().filter(funcionario = self.usuario).filter(data = f'{self.ano}-{self.mes}-{dia}')
            
            res = ''

            if data:
               
              res = f'<td class="{data[0].status}"><span class="date">{dia}</span></td>'
            
            else:

                if self.data_atual.day == dia and self.data_atual.month == self.mes and self.data_atual.year == self.ano:

                    res = f'<td class= "dia_atual"><span class="date">{dia}</span></td>'

                else:    
                    
                    res = f'<td><span class="date">{dia}</span></td>'
            return res

        return '<td></td>'

    def formatweek(self, dia_semana):

        semana = ''

        for dia , sem in dia_semana:

            semana += self.formatday(dia)
        
        return f'<tr> {semana} </tr>'

    def formatmonthname(self, theyear, themonth, withyear=True):
       
        
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]
        return '<tr><th colspan="7" class="%s">%s</th></tr>' % (
            'header-mes', s)
    
        

    def formatweekday(self, day):
       
        return '<th class="%s">%s</th>' % (
            self.cssclasses_weekday_head[day], day_abbr[day])


    def formatweekheader(self):
        
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        return '<tr>%s</tr>' % s

    def formatmonth(self, withyear = True):

        calendario = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        calendario += f'{self.formatmonthname(self.ano, self.mes, withyear=withyear)}\n'
        calendario += f'{self.formatweekheader()}\n'
		
        for week in self.monthdays2calendar(self.ano, self.mes):
		    
            calendario += f'{self.formatweek(week)}\n'
        
        calendario += '</table>\n'
        return calendario
