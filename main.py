from flet import *
import os
import asyncio
from prisma import Client


# SET OS ENVIRON
os.environ['PRISMA_DATASOURCES'] = "default = sqlite:///db/dbmain.db"

prisma = Client()




async def main(page:Page):

	# OPEN CONNECTION TO DATABASE
	await prisma.connect()


	nametxt = TextField(label="username")
	agetxt = TextField(label="age")
	myid = Text()

	mytable = DataTable(
		columns=[
		DataColumn(Text("actions")),
		DataColumn(Text("id")),
		DataColumn(Text("name")),
		DataColumn(Text("age")),
			],
			rows=[]

		)


	async def saveedit(e):
		await prisma.user.update(
			where={"id":myid.value},
			data={"name":nametxt.value,
				"age":int(agetxt.value)
				}
			)

		# AND CLOSE YOU DIALOG EDIT AND REFRESH AGAIN TABLE
		mydialog.open = False
		mytable.rows.clear()
		await read_all_data()
		await page.update_async()

	# CREATE DIALOG FOR EDIT YOU
	mydialog = AlertDialog(
		title=Text("Edit data"),
		content=Column([
			nametxt,
			agetxt
			]),
		actions=[
			ElevatedButton("save data",
				bgcolor="blue",color="white",
				on_click=saveedit
				)

			],
		actions_alignment="end"


		)


	# EDIT BUTTON
	async def editbtn(e):
		# AND GET LAST NAME AND AGE VALUE
		nametxt.value = e.control.data.name
		agetxt.value = e.control.data.age
		myid.value = e.control.data.id

		# OPEN THE DIALOG FOR EDIT NAME AND AGE
		page.dialog = mydialog 
		mydialog.open = True
		await page.update_async()


	# DELETE FUNCTION
	async def deletebtn(e):
		# YOU DELETE ID 
		delid = e.control.data
		await prisma.user.delete(where={"id":delid})
		mytable.rows.clear()
		await read_all_data()
		await page.update_async()


	# GET ALL DATA FROM DATABASE
	async def read_all_data():
		users = await prisma.user.find_many()
		# AND LOOP AND PUSH TO WIDGET DATATABLAE
		for user in users:
			mytable.rows.append(
				DataRow(
					cells=[
						# CREATE EDIT AND DELETE BUTTON
					DataCell(Row([
						IconButton("create",
							icon_color="blue",
							data=user,
							on_click=editbtn
							),
						IconButton("delete",
							icon_color="red",
							data=user.id,
							on_click=deletebtn
							)


						])),
					DataCell(Text(user.id)),
					DataCell(Text(user.name)),
					DataCell(Text(user.age)),


						]

					)

				)



	# CALL FUCNTION
	await read_all_data()


	async def create_record(e):
		try:
			res = await prisma.user.create(
				{
					"name":nametxt.value,
					"age":int(agetxt.value)
				}
				)
			print("success",res)
		except Exception as e:
			print(e)
			print("ERRROR CHECK !!!!")

		# AND CLEAR TABLE AND CALL FUNCTIO AGAIN
		mytable.rows.clear()
		await read_all_data()
		# AND UPDATE PAGE
		await page.update_async()




	await page.add_async(
		Column([
		nametxt,
		agetxt,
		ElevatedButton("send",
			bgcolor="blue",color="white",
			on_click=create_record
			),

		Row([mytable],scroll="always")

			])
		)

flet.app(target=main)
